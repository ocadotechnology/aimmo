#!/usr/bin/env python
import logging
import os

from game_manager import GAME_MANAGERS

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.Logger()

LOGGER.critical("I SHOULD PRINT OUT AND NOTHING ELSE")
