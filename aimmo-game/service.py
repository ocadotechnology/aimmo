#!/usr/bin/env python

import ast
import asyncio
import json
import logging
import os
import signal
import sys
from urllib.parse import parse_qs

import aiohttp
import aiohttp_cors
import socketio
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from prometheus_client import make_wsgi_app

from activity_monitor import ActivityMonitor, StatusOptions
from authentication import initialize_game_token
from simulation import map_generator
from simulation.django_communicator import DjangoCommunicator
from simulation.game_runner import GameRunner

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

django_api_url = os.environ.get(
    "GAME_API_URL", "http://localhost:8000/aimmo/api/games/"
)

communicator = DjangoCommunicator(
    django_api_url=django_api_url, completion_url=django_api_url + "complete/"
)
activity_monitor = ActivityMonitor(communicator)


def app_setup(should_clean_token=True):
    async def clean_token(app):
        LOGGER.info("Cleaning token!")
        await communicator.patch_token(data={"token": ""})

    app = web.Application()

    wsgi_handler = WSGIHandler(make_wsgi_app())
    app.add_routes([web.get("/{path_info:metrics}", wsgi_handler)])

    if should_clean_token:
        app.on_shutdown.append(clean_token)

    app.on_shutdown.append(communicator.close_session)

    return app


def socketIO_setup(
    app, client_manager_class=socketio.AsyncManager, async_handlers=True
):
    socket_server = socketio.AsyncServer(
        client_manager=client_manager_class(), async_handlers=async_handlers
    )

    socket_server.attach(
        app, socketio_path=os.environ.get("SOCKETIO_RESOURCE", "socket.io")
    )

    return socket_server


app = app_setup()
cors = aiohttp_cors.setup(app)

socketio_server = socketIO_setup(app)


class GameAPI(object):

    routes = web.RouteTableDef()

    def __init__(self, game_state, worker_manager, web_app=app, socketio_server2=socketio_server):
        self.app = web_app
        self.socketio_server = socketio_server2
        self.register_endpoints()
        self.worker_manager = worker_manager
        self.game_state = game_state

    async def async_map(self, func, iterable_args):
        futures = [func(arg) for arg in iterable_args]
        await asyncio.gather(*futures)

    def register_endpoints(self):
        self.register_player_data_view()
        self.register_world_update_on_connect()
        self.register_remove_session_id_from_mappings()
        self.register_healthcheck()
        self.app.add_routes(self.routes)

    def open_connections(self):
        try:
            return self.socketio_server.manager.get_participants("/", None)
        except KeyError:
            return None

    def update_active_users(self):
        activity_monitor.active_users = len(self.socketio_server.eio.sockets)

    def register_healthcheck(self):
        @self.routes.get("/game-{game_id}")
        async def healthcheck(request):
            return web.Response(text="HEALTHY")

        return healthcheck

    def register_player_data_view(self):
        @self.routes.get("/player/{player_id}")
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
        @self.socketio_server.on("connect")
        async def world_update_on_connect(sid, environ):
            query = environ["QUERY_STRING"]
            avatar_id = self._find_avatar_id_from_query(sid, query)
            await self.socketio_server.save_session(sid, {"id": avatar_id})
            self.update_active_users()
            await self.send_updates(sid)

        return world_update_on_connect

    def register_remove_session_id_from_mappings(self):
        @self.socketio_server.on("disconnect")
        async def remove_session_id_from_mappings(sid):
            print(f"This is a disconnect: {sid}")
            LOGGER.info("Socket disconnected for session id:{}. ".format(sid))
            self.update_active_users()

        return remove_session_id_from_mappings

    async def send_updates(self, sid):
        await self._send_have_avatars_code_updated(sid)
        print("avatars code updated")
        await self._send_game_state(sid)
        print("game state sent")
        await self._send_logs(sid)
        print("logs sent")

    async def send_updates_to_all(self):
        try:
            socket_ids = self.socketio_server.manager.get_participants("/", None)
            await self.async_map(self.send_updates, socket_ids)
        except KeyError:
            LOGGER.error("No open socket connections")

    def _find_avatar_id_from_query(self, session_id, query_string):
        """
        :param session_id: Int with the session id
        :param query_string: String from the environment settings,
        usually located as the key 'QUERY_STRING'.
        """
        parsed_qs = parse_qs(query_string)

        try:
            avatar_id = int(parsed_qs["avatar_id"][0])
            return avatar_id
        except ValueError:
            LOGGER.error("Avatar ID could not be casted into an integer")
        except KeyError:
            LOGGER.error("No avatar ID found. User may not be authorised")
            LOGGER.error("query_string: " + query_string)

    async def _send_logs(self, sid):
        def should_send_logs(logs):
            return bool(logs)

        session_data = await self.socketio_server.get_session(sid)
        worker = self.worker_manager.player_id_to_worker[session_data["id"]]
        avatar_logs = worker.log

        if should_send_logs(avatar_logs):
            await self.socketio_server.emit(
                "log",
                {"message": avatar_logs, "turn_count": self.game_state.turn_count},
                room=sid,
            )

    async def _send_game_state(self, sid):
        serialized_game_state = self.game_state.serialize()
        await self.socketio_server.emit("game-state", serialized_game_state, room=sid)

    async def _send_have_avatars_code_updated(self, sid):
        session_data = await self.socketio_server.get_session(sid)
        worker = self.worker_manager.player_id_to_worker[session_data["id"]]
        if worker.has_code_updated:
            await self.socketio_server.emit("feedback-avatar-updated", {}, room=sid)


def create_runner(port):
    settings = json.loads(os.environ["settings"])
    generator = getattr(map_generator, settings["GENERATOR"])(settings)
    return GameRunner(
        game_state_generator=generator.get_game_state,
        communicator=communicator,
        port=port,
    )


def run_game(port):
    game_runner = create_runner(port)

    game_api = GameAPI(
        game_state=game_runner.game_state, worker_manager=game_runner.worker_manager
    )
    game_runner.set_end_turn_callback(game_api.send_updates_to_all)
    asyncio.ensure_future(game_runner.run())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    host = sys.argv[1]

    if os.environ["WORKER"] == "local":
        port = int(os.environ["EXTERNAL_PORT"])
    else:
        port = int(sys.argv[2])

    asyncio.ensure_future(initialize_game_token(communicator))
    run_game(port)

    logging.getLogger("socketio").setLevel(logging.ERROR)
    logging.getLogger("engineio").setLevel(logging.ERROR)
    LOGGER.info("starting the server")
    LOGGER.info(app.router)
    web.run_app(app, host=host, port=port)
