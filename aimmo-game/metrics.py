from prometheus_client import Histogram, Gauge, Summary, Counter
import os

# This files contains the definitions of all the custom metrics we currently measure.
# Any new metrics needed should be stored here. In addition, when dealing with async code
# you should use the context manager approach instead of decorators when using the metrics
# as decoraters do not function properly with async code.

# Measures the time taken for the game to go through an entire turn (game runner's update method)
CUSTOM_BUCKET = [0.0, 0.25,0.5,0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5
                ,2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0]
GAME_TURN_PROCESSING_SECONDS = Histogram('function_exec_time', 'Test metric to see if we can time a functions execution',
                        buckets=CUSTOM_BUCKET,
                        labelnames=('game_id'),
                        labelvalues=(f'{os.environ['GAME_ID']))
