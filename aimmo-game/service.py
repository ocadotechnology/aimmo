#!/usr/bin/env python

import ast
import asyncio
import json
import logging
import os
import pickle
import sys
from urllib.parse import parse_qs

import aiohttp_cors
import socketio
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from prometheus_client import make_wsgi_app

from activity_monitor import ActivityMonitor
from simulation import map_generator
from simulation.game_runner import GameRunner

app = web.Application()
cors = aiohttp_cors.setup(app)


async def callback(self):
    LOGGER.info("Timer expired! Game marked as STOPPED")
    # this should trigger the game for deletion, part of (#1011)


activity_monitor = ActivityMonitor(callback)
socketio_server = socketio.AsyncServer(async_handlers=True)

routes = web.RouteTableDef()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GameAPI(object):
    def __init__(self, game_state, worker_manager):
        self._socket_session_id_to_player_id = {}
        self.register_endpoints()
        self.worker_manager = worker_manager
        self.game_state = game_state

    def register_endpoints(self):
        self.register_player_data_view()
        self.register_world_update_on_connect()
        self.register_remove_session_id_from_mappings()
        self.register_healthcheck()
        app.add_routes(routes)

    def register_healthcheck(self):
        @routes.get("/game-{game_id}")
        async def healthcheck(request):
            return web.Response(text="HEALTHY")

        return healthcheck

    def register_player_data_view(self):
        @routes.get("/player/{player_id}")
        async def player_data(request: web.Request):
            player_id = int(request.match_info["player_id"])
            return web.json_response(
                {
                    "code": self.worker_manager.get_code(player_id),
                    "options": {},
                    "state": None,
                }
            )

        return player_data

    def register_world_update_on_connect(self):
        @socketio_server.on("connect")
        async def world_update_on_connect(sid, environ):
            query = environ["QUERY_STRING"]
            self._find_avatar_id_from_query(sid, query)
            activity_monitor.active_users = len(self._socket_session_id_to_player_id)
            await self.send_updates()

        return world_update_on_connect

    def register_remove_session_id_from_mappings(self):
        @socketio_server.on("disconnect")
        async def remove_session_id_from_mappings(sid):
            LOGGER.info("Socket disconnected for session id:{}. ".format(sid))
            try:
                del self._socket_session_id_to_player_id[sid]
                activity_monitor.active_users = len(
                    self._socket_session_id_to_player_id
                )
            except KeyError:
                pass

        return remove_session_id_from_mappings

    async def send_updates(self):
        player_id_to_worker = self.worker_manager.player_id_to_worker
        await self._send_have_avatars_code_updated(player_id_to_worker)
        await self._send_game_state()
        await self._send_logs(player_id_to_worker)

    def _find_avatar_id_from_query(self, session_id, query_string):
        """
        :param session_id: Int with the session id
        :param query_string: String from the environment settings,
        usually located as the key 'QUERY_STRING'.
        """
        parsed_qs = parse_qs(query_string)

        try:
            avatar_id = int(parsed_qs["avatar_id"][0])
            self._socket_session_id_to_player_id[session_id] = avatar_id
        except ValueError:
            LOGGER.error("Avatar ID could not be casted into an integer")
        except KeyError:
            LOGGER.error("No avatar ID found. User may not be authorised ")
            LOGGER.error("query_string: " + query_string)

    async def _send_logs(self, player_id_to_workers):
        def should_send_logs(logs):
            return bool(logs)

        socket_session_id_to_player_id_copy = (
            self._socket_session_id_to_player_id.copy()
        )
        for sid, player_id in socket_session_id_to_player_id_copy.items():
            avatar_logs = player_id_to_workers[player_id].log
            if should_send_logs(avatar_logs):
                await socketio_server.emit("log", avatar_logs, room=sid)

    async def _send_game_state(self):
        serialized_game_state = self.game_state.serialize()
        socket_session_id_to_player_id_copy = (
            self._socket_session_id_to_player_id.copy()
        )
        for sid, player_id in socket_session_id_to_player_id_copy.items():
            await socketio_server.emit("game-state", serialized_game_state, room=sid)

    async def _send_have_avatars_code_updated(self, player_id_to_workers):
        socket_session_id_to_player_id_copy = (
            self._socket_session_id_to_player_id.copy()
        )
        for sid, player_id in socket_session_id_to_player_id_copy.items():
            if player_id_to_workers[player_id].has_code_updated:
                await socketio_server.emit("feedback-avatar-updated", {}, room=sid)


def create_runner(port):
    settings = json.loads(os.environ["settings"])
    generator = getattr(map_generator, settings["GENERATOR"])(settings)
    return GameRunner(
        game_state_generator=generator.get_game_state,
        django_api_url=os.environ.get(
            "GAME_API_URL", "http://localhost:8000/aimmo/api/games/"
        ),
        port=port,
    )


def run_game(port):
    game_runner = create_runner(port)
    game_api = GameAPI(
        game_state=game_runner.game_state, worker_manager=game_runner.worker_manager
    )
    game_runner.set_end_turn_callback(game_api.send_updates)
    asyncio.ensure_future(game_runner.run())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    host = sys.argv[1]

    socketio_server.attach(
        app, socketio_path=os.environ.get("SOCKETIO_RESOURCE", "socket.io")
    )

    if os.environ["WORKER"] == "local":
        port = int(os.environ["EXTERNAL_PORT"])
    else:
        port = int(sys.argv[2])

    run_game(port)

    wsgi_handler = WSGIHandler(make_wsgi_app())
    app.add_routes([web.get("/{path_info:metrics}", wsgi_handler)])

    LOGGER.info("starting the server")
    web.run_app(app, host=host, port=port)
