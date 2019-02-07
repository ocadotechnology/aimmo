from prometheus_client import Histogram, Gauge, Summary, Counter
import os

# This files contains the definitions of all the custom metrics we currently measure.
# Any new metrics needed should be stored here. In addition, when dealing with async code
# you should use the context manager approach instead of decorators. When using the metrics
# as decoraters do not function properly with async code.

# Do not use a metric more than once, it will probably break them. If you need to measure
# something in a similar or the same way as an existing metric, create a new one.

# Measures the time taken for the game to go through an entire turn (game runner's update method)
CUSTOM_BUCKET = [x/10 for x in range(10,101)]
GAME_TURN = Histogram('game_turn_time', 'Measures the time taken for the game to complete a single turn in seconds',
                        buckets=CUSTOM_BUCKET)
def GAME_TURN_TIME():
    """ Used for measuring the time it games for the game to complete a turn. This is stored
        on a Histogram with values 1 to 5 +infinity going in steps of 0.1. """
    return GAME_TURN.time()
