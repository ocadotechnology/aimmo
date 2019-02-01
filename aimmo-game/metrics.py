from prometheus_client import Histogram, Gauge, Summary, Counter
import os

# This files contains the definitions of all the custom metrics we currently measure.
# Any new metrics needed should be stored here. In addition, when dealing with async code
# you should use the context manager approach instead of decorators. When using the metrics
# as decoraters do not function properly with async code.

# Measures the time taken for the game to go through an entire turn (game runner's update method)
def GAME_TURN_PROCESSING_SECONDS():
    CUSTOM_BUCKET = [x/10 for x in range(10,51)] 
    return Histogram('function_exec_time', 'Test metric to see if we can time a functions execution',
                        buckets=CUSTOM_BUCKET,
                        labelnames=('game_id'),
                        labelvalues=(f'{os.environ['GAME_ID']))

