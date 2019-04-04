from prometheus_client import Histogram
import os

# DO NOT use a metric more than once, it will probably break them. If you need to measure
# something in a similar or the same way as an existing metric, create a new one.

# Measures the time taken for the game to go through an entire turn (game runner's update method)
CUSTOM_BUCKET = [x / 10 for x in range(10, 61)]
GAME_TURN = Histogram(
    "game_turn_time",
    "Measures the time taken for the game to complete a single turn in seconds",
    buckets=CUSTOM_BUCKET,
)


def GAME_TURN_TIME():
    """
    Use for measuring the time it games for the game to complete a turn.

    This is measured using the Histogram datatype.
    """
    return GAME_TURN.time()
