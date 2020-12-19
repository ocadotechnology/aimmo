#!/usr/bin/env python

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict
from urllib.parse import parse_qs

import aiohttp_cors
import google.cloud.logging
import grpc
import nest_asyncio
import socketio
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from google.auth.exceptions import DefaultCredentialsError
from kubernetes.config import load_incluster_config
from prometheus_client import make_wsgi_app

from activity_monitor import ActivityMonitor
from agones import sdk_pb2
from agones.sdk_pb2_grpc import SDKStub as AgonesSDKStub
from authentication import initialize_game_token
from simulation import map_generator
from simulation.django_communicator import DjangoCommunicator
from simulation.game_runner import GameRunner
from simulation.log_collector import LogCollector
from turn_collector import TurnCollector

nest_asyncio.apply()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


channel = grpc.aio.insecure_channel(f"localhost:{os.environ['AGONES_SDK_GRPC_PORT']}")
agones_stub = AgonesSDKStub(channel)


def setup_application(communicator: DjangoCommunicator, should_clean_token=True):
    async def clean_token(app):
        LOGGER.info("Cleaning token!")
        await communicator.patch_token(data={"token": ""})

    application = web.Application()

    if should_clean_token:
        application.on_shutdown.append(clean_token)

    application.on_shutdown.append(communicator.close_session)

    return application


# def setup_prometheus():
#     wsgi_handler = WSGIHandler(make_wsgi_app())
#     app.add_routes([web.get("/{path_info:metrics}", wsgi_handler)])


def setup_socketIO_server(application, async_handlers=True):
    socket_server = socketio.AsyncServer(
        async_mode="aiohttp",
        client_manager=socketio.AsyncManager(),
        async_handlers=async_handlers,
        cors_allowed_origins=[
            "http://localhost:8000",
            "https://dev-dot-decent-digit-629.appspot.com",
            "https://staging-dot-decent-digit-629.appspot.com",
            "https://www.codeforlife.education",
        ],
    )

    socket_server.attach(
        application, socketio_path=os.environ.get("SOCKETIO_RESOURCE", "socket.io")
    )

    return socket_server


class GameAPI(object):
    def __init__(self, game_state, application, socketio_server):
        self.app = application
        self.socketio_server = socketio_server
        self.register_endpoints()
        self.game_state = game_state
        self.log_collector = LogCollector(game_state.avatar_manager)

    async def async_map(self, func, iterable_args):
        futures = [func(arg) for arg in iterable_args]
        await asyncio.gather(*futures)

    def register_endpoints(self):
        self.routes = web.RouteTableDef()
        self.register_healthcheck()
        self.register_world_update_on_connect()
        self.register_remove_session_id_from_mappings()
        self.app.add_routes(self.routes)

    def open_connections_number(self):
        try:
            return len(
                [x for x in self.socketio_server.manager.get_participants("/", None)]
            )
        except KeyError:
            return 0

    def update_active_users(self):
        activity_monitor.active_users = self.open_connections_number()

    def register_healthcheck(self):
        @self.routes.get("/game-{game_id}")
        async def healthcheck(request):
            return web.Response(text="HEALTHY")

        return healthcheck

    def register_world_update_on_connect(self):
        @self.socketio_server.on("connect")
        async def world_update_on_connect(sid, environ):
            LOGGER.info(f"Socket connected for session id: {sid}")
            query = environ["QUERY_STRING"]
            avatar_id = self._find_avatar_id_from_query(sid, query)
            await self.socketio_server.save_session(sid, {"id": avatar_id})

        return world_update_on_connect

    def register_remove_session_id_from_mappings(self):
        @self.socketio_server.on("disconnect")
        async def remove_session_id_from_mappings(sid):
            LOGGER.info("Socket disconnected for session id: {}. ".format(sid))

        return remove_session_id_from_mappings

    async def send_updates(self, sid):
        try:
            await self._send_game_state(sid)
        except KeyError:
            LOGGER.error(
                f"Failed to send updates. No worker for player in session {sid}"
            )

    async def send_updates_to_all(self):
        try:
            socket_ids = self.socketio_server.manager.get_participants("/", None)
            await self.async_map(self.send_updates, socket_ids)
        except KeyError as e:
            LOGGER.warning("No open socket connections")
        self.update_active_users()

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
            LOGGER.error(f"query_string: {query_string}")

    async def _send_game_state(self, sid):
        session_data = await self.socketio_server.get_session(sid)
        serialized_game_state = self.game_state.serialize()
        serialized_game_state["playerLog"] = self.log_collector.collect_logs(
            session_data["id"]
        )
        await self.socketio_server.emit("game-state", serialized_game_state, room=sid)


def create_runner(port, socketio_server, communicator: DjangoCommunicator):
    generator = map_generator.Main({})
    turn_collector = TurnCollector(socketio_server)
    return GameRunner(
        game_state_generator=generator.get_game_state,
        communicator=communicator,
        port=port,
        turn_collector=turn_collector,
    )


future_app = asyncio.Future()
future_port = asyncio.Future()


def run_game(port, game_id, django_api_url):
    global activity_monitor
    global cors
    global communicator

    LOGGER.info("got to run game")
    communicator = DjangoCommunicator(django_api_url=django_api_url)
    activity_monitor = ActivityMonitor(communicator, agones_stub)

    app = setup_application(communicator)
    cors = aiohttp_cors.setup(app)
    socketio_server = setup_socketIO_server(app)

    game_runner = create_runner(port, socketio_server, communicator)

    asyncio.ensure_future(initialize_game_token(communicator, game_id))

    game_api = GameAPI(
        game_state=game_runner.game_state,
        application=app,
        socketio_server=socketio_server,
    )
    game_runner.set_end_turn_callback(game_api.send_updates_to_all)

    asyncio.ensure_future(game_runner.run())
    # run_server(app)
    LOGGER.info("setting the future app")
    # try:
    future_app.set_result(app)
    # except asyncio.base_futures.InvalidStateError:
    #     pass


async def watch_for_updates():
    is_already_allocated = False
    LOGGER.info("starting to watch for updates")
    empty_request = sdk_pb2.Empty()
    async for game_server_update in agones_stub.WatchGameServer(empty_request):
        if game_server_update.status.state == "Allocated" and not is_already_allocated:
            LOGGER.info("NEW GAME SERVER UPDATE!")
            LOGGER.info(game_server_update)
            is_already_allocated = True
            labels: Dict[str, Any] = game_server_update.object_meta.labels
            annotations: Dict[str, Any] = game_server_update.object_meta.annotations
            game_id = labels["game-id"]
            os.environ["worksheet_id"] = labels["worksheet_id"]
            os.environ["GAME_API_URL"] = annotations["game-api-url"]
            django_api_url = annotations["game-api-url"]
            port = 5000
            run_game(port, game_id, django_api_url)


def setup_healthcheck():
    def empty_response_generator():
        while True:
            emp_request = sdk_pb2.Empty()
            LOGGER.debug("sending healthcheck")
            yield emp_request

    agones_stub.Health(empty_response_generator())


def send_ready_state():
    empty_request = sdk_pb2.Empty()
    agones_stub.Ready(empty_request)


async def get_app():
    app = await future_app
    LOGGER.info(f"we have an app: {app}")
    return app


async def run_server():
    port = 5000
    host = sys.argv[1]
    LOGGER.info(f"this is the host: {host}")
    web.run_app(get_app(), port=port)


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)
    try:
        logging_client = google.cloud.logging.Client()
        logging_client.get_default_handler()
        logging_client.setup_logging()
    except DefaultCredentialsError:
        logging.info(
            "No google credentials provided, not connecting google logging client"
        )


if __name__ == "__main__":
    load_incluster_config()
    setup_logging()
    LOGGER.info("running")
    setup_healthcheck()
    LOGGER.info("setup healthcheck")
    asyncio.ensure_future(watch_for_updates())
    LOGGER.info("setup watch handler")
    send_ready_state()

    # setup_prometheus()
    LOGGER.info("running web server eventually")
    asyncio.get_event_loop().run_until_complete(run_server())

    logging.getLogger("socketio").setLevel(logging.ERROR)
    logging.getLogger("engineio").setLevel(logging.ERROR)
    logging.getLogger("aiohttp.server").setLevel(logging.DEBUG)
