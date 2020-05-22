#!/usr/bin/env python
import json

import aiohttp_cors
import logging
import sys
from aiohttp import web

from avatar_runner import AvatarRunner
from code_updater import CodeUpdater
from simulation.avatar_state import AvatarState
from simulation.world_map import WorldMap, WorldMapCreator

app = web.Application()
cors = aiohttp_cors.setup(app)

routes = web.RouteTableDef()

LOGGER = logging.getLogger(__name__)

avatar_runner = None
code_updater = None
DATA_URL = ""


@routes.post("/turn/")
async def process_turn(request):
    data = json.loads(await request.content.read())
    world_map = WorldMapCreator.generate_world_map_from_cells_data(**data["world_map"])
    code, options = data["code"], data["options"]
    avatar_state = AvatarState(
        location=data["avatar_state"]["location"],
        score=data["avatar_state"]["score"],
        health=data["avatar_state"]["health"],
        backpack=data["avatar_state"]["backpack"],
        id=0,
        orientation="north",
    )

    response = avatar_runner.process_avatar_turn(world_map, avatar_state, code)
    return web.json_response(response)


def run(host, port, data_url):
    global avatar_runner, DATA_URL
    DATA_URL = data_url
    logging.basicConfig(level=logging.DEBUG)
    code_updater = CodeUpdater()
    avatar_runner = AvatarRunner(code_updater=code_updater)
    app.add_routes(routes)
    LOGGER.info("STARTING THE SERVER.")
    LOGGER.info(f"RUNNING ON: (host: {host}, port: {port})")
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    run(host=sys.argv[1], port=int(sys.argv[2]), data_url=sys.argv[3])
