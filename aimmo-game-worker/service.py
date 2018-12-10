#!/usr/bin/env python
import logging
import sys
import json
import timeit
import flask
import requests
from aiohttp import web
import aiohttp_cors
import asyncio

from simulation.avatar_state import AvatarState
from simulation.world_map import WorldMap
from avatar_runner import AvatarRunner

app = web.Application()
cors = aiohttp_cors.setup(app)

routes = web.RouteTableDef()

LOGGER = logging.getLogger(__name__)

avatar_runner = None
DATA_URL = ''


def get_code_and_options():
    data = requests.get(DATA_URL).json()
    return data['code'], data['options']


@routes.post('/turn/')
async def process_turn(request):
    code, options = get_code_and_options()
    data = json.loads(await request.content.read())
    world_map = WorldMap(**data['world_map'])
    code, options = data['code'], data['options']
    avatar_state = AvatarState(location=data['avatar_state']['location'],
                               score=data['avatar_state']['score'],
                               health=data['avatar_state']['health'])

    response = avatar_runner.process_avatar_turn(world_map, avatar_state, code)
    LOGGER.info(f"I TOOK THIS LONG TO SEND MY FIRST REQUEST: {timeit.default_timer() - start}")
    return web.json_response(response)


def run(host, port, data_url):
    global avatar_runner, DATA_URL
    DATA_URL = data_url
    logging.basicConfig(level=logging.DEBUG)
    avatar_runner = AvatarRunner()
    app.add_routes(routes)
    web.run_app(app, host=host, port=port)
    LOGGER.info(f"I TOOK THIS LONG TO START UP: {timeit.default_timer() - start}")
    LOGGER.info("HI!")


if __name__ == '__main__':
    start = timeit.default_timer()
    run(host=sys.argv[1], port=int(sys.argv[2]), data_url=sys.argv[3])
