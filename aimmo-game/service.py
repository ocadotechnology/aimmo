#!/usr/bin/env python

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Awaitable, Dict
from urllib.parse import parse_qs

import aiohttp_cors
import google.cloud.logging
import grpc
import socketio
from aiohttp import web
from google.auth.exceptions import DefaultCredentialsError
from kubernetes.config import load_incluster_config
from socketio.asyncio_server import AsyncServer

from activity_monitor import ActivityMonitor
from agones import sdk_pb2
from agones.sdk_pb2_grpc import SDKStub as AgonesSDKStub
from authentication import initialize_game_token
from simulation import map_generator
from simulation.django_communicator import DjangoCommunicator
from simulation.game_runner import GameRunner
from simulation.log_collector import LogCollector
from turn_collector import TurnCollector

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def setup_application(communicator: DjangoCommunicator, should_clean_token=True):
    async def clean_token(app):
        LOGGER.info("Cleaning token!")
        await communicator.patch_token(data={"token": ""})

    application = web.Application()

    if should_clean_token:
        application.on_shutdown.append(clean_token)

    application.on_shutdown.append(communicator.close_session)

    return application


def setup_socketIO_server(application, async_handlers=True):
    socket_server = AsyncServer(
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
    def __init__(
        self,
        game_state,
        application,
        socketio_server: AsyncServer,
        activity_monitor: ActivityMonitor,
    ):
        self.app = application
        self.socketio_server = socketio_server
        self.register_endpoints()
        self.game_state = game_state
        self.log_collector = LogCollector(game_state.avatar_manager)
        self.activity_monitor = activity_monitor

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
        self.activity_monitor.active_users = self.open_connections_number()

    def register_healthcheck(self):
        @self.routes.get("/game-{game_id}")
        async def healthcheck(request):
            return web.Response(text="HEALTHY")

        return healthcheck

    def register_world_update_on_connect(self):
        @self.socketio_server.on("connect")
        async def world_update_on_connect(sid, environ):
            query = environ["QUERY_STRING"]
            avatar_id = self._find_avatar_id_from_query(sid, query)
            await self.socketio_server.save_session(sid, {"id": avatar_id})
            LOGGER.info(f"Socket connected for session id: {sid}")

        return world_update_on_connect

    def register_remove_session_id_from_mappings(self):
        @self.socketio_server.on("disconnect")
        async def remove_session_id_from_mappings(sid):
            LOGGER.info("Socket disconnected for session id: {}. ".format(sid))

        return remove_session_id_from_mappings

    async def send_updates(self, sid):
        try:
            LOGGER.info(f"sending updates to {sid}")
            await self._send_game_state(sid)
        except KeyError as e:
            LOGGER.error(f"Failed to send updates: {e}")

    async def send_updates_to_all(self):
        try:
            socket_ids = [
                sid
                for (sid, _) in self.socketio_server.manager.get_participants("/", None)
            ]
            LOGGER.info(f"socket_ids: f{socket_ids}")
            await self.async_map(self.send_updates, socket_ids)
        except KeyError as e:
            LOGGER.warning("No open socket connections")
            LOGGER.error(e)
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
    settings = json.loads(os.environ["settings"])
    generator = getattr(map_generator, settings["GENERATOR"])(settings)
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
    global cors

    communicator = DjangoCommunicator(django_api_url=django_api_url)
    activity_monitor = ActivityMonitor(communicator)

    app = setup_application(communicator)
    cors = aiohttp_cors.setup(app)
    socketio_server = setup_socketIO_server(app)

    game_runner = create_runner(port, socketio_server, communicator)

    asyncio.ensure_future(initialize_game_token(communicator, game_id))

    game_api = GameAPI(
        game_state=game_runner.game_state,
        application=app,
        socketio_server=socketio_server,
        activity_monitor=activity_monitor,
    )
    game_runner.set_end_turn_callback(game_api.send_updates_to_all)

    asyncio.ensure_future(game_runner.run())
    future_app.set_result(app)


@dataclass
class GameAllocationInfo:
    game_id: int
    django_api_url: str
    port: int = 5000


async def wait_for_allocation(
    agones_stub: AgonesSDKStub,
) -> Awaitable[GameAllocationInfo]:
    empty_request = sdk_pb2.Empty()
    async for game_server_update in agones_stub.WatchGameServer(empty_request):
        if game_server_update.status.state == "Allocated":
            LOGGER.info(f"Game server allocated")
            labels: Dict[str, Any] = game_server_update.object_meta.labels
            annotations: Dict[str, Any] = game_server_update.object_meta.annotations
            game_id = labels["game-id"]
            os.environ["worksheet_id"] = annotations["worksheet_id"]
            os.environ["GAME_API_URL"] = annotations["GAME_API_URL"]
            os.environ["settings"] = annotations["settings"]
            django_api_url = annotations["GAME_API_URL"]
            return GameAllocationInfo(game_id, django_api_url)


def setup_healthcheck(agones_stub: AgonesSDKStub):
    def empty_response_generator():
        while True:
            emp_request = sdk_pb2.Empty()
            yield emp_request

    agones_stub.Health(empty_response_generator())


def send_ready_state(agones_stub: AgonesSDKStub):
    empty_request = sdk_pb2.Empty()
    agones_stub.Ready(empty_request)
    LOGGER.info("Game server ready for allocation")


async def get_app():
    app = await future_app
    return app


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)

    logging.getLogger("socketio").setLevel(logging.ERROR)
    logging.getLogger("engineio").setLevel(logging.ERROR)
    logging.getLogger("aiohttp.server").setLevel(logging.INFO)

    try:
        logging_client = google.cloud.logging.Client()
        logging_client.get_default_handler()
        logging_client.setup_logging()
    except DefaultCredentialsError:
        logging.info(
            "No google credentials provided, not connecting google logging client"
        )


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    channel = grpc.aio.insecure_channel(
        f"localhost:{os.environ['AGONES_SDK_GRPC_PORT']}",
        options=(("grpc.enable_http_proxy", 0),),
    )
    agones_stub = AgonesSDKStub(channel)
    load_incluster_config()
    setup_logging()
    setup_healthcheck(agones_stub)
    send_ready_state(agones_stub)
    game_metadata: GameAllocationInfo = event_loop.run_until_complete(
        wait_for_allocation(agones_stub)
    )

    run_game(game_metadata.port, game_metadata.game_id, game_metadata.django_api_url)
    web.run_app(get_app(), port=game_metadata.port)
