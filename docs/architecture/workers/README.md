# Workers (`aimmo-game-worker` directory)

---

The game worker is subordinated to the [game](game). The worker has two components: initialization and the service.

### The initialization 

The initialization of the worker has the responsibility of getting the user code and a set of options that the avatar uses at initialization. When the user updates the code in the [code editor](https://ace.c9.io/), the code gets saved in the database. 

Updating the code of a user is done with the help of the database through the [game API](game-api). The game API resource for getting the code and for posting new code is shared: when a GET is made, we receive the avatar code, a POST is made, we update the avatar code.

The code and options are saved inside a directory. The directory is built when the `initilise.py` file is executed. The [LocalWorkerManager](worker-manager)(from [Game](game)) does not call the `initialise.py` file, updating the files by hand, then running the `service.py`. The [KubernetesWorkerManager](worker-manger)(from [Game](game)) run both functions by running the shell file `run.sh`.

```shell
set -e
dir=$(mktemp -d)
python ./initialise.py $dir
export PYTHONPATH=$dir:$PYTHONPATH
exec python ./service.py $1 $2 $dir
```

The API call is made indirectly by calling a resource exposed inside the [Game's Flask Service](flask-microservice). This resource's URL would looks something like `http://game-5/player/1`. Worker manager's `get_code` method does a get at the [API](game-api) resource `code`. _As we can observe, the options json file is not yet used._

```python
@app.route('/player/<player_id>')
def player_data(player_id):
    player_id = int(player_id)
    return flask.jsonify({
        'code': worker_manager.get_code(player_id),
        'options': {},       
        'state': None,
    })
```



### The service 

The service runs after the avatar code has been imported from the database as explained above.

Each worker listens to POST requests for processing a turn. The data that the worker receives has the form of a **world map** and an **avatar state**. The user's code is retrieved from the directory that was built during the initialization phase. (see `run.py` above)

```python
from avatar import Avatar
global worker_avatar
worker_avatar = Avatar(**options)
```

The service assumes the user's `Avatar` class implements the method `handle_turn` and acts accordingly:

```python
@app.route('/turn/', methods=['POST'])
def process_turn():
   [...]
   action = worker_avatar.handle_turn(avatar_state, world_map)
   return flask.jsonify(action=action.serialise())
```

The simulation is different for the worker from the simulation of the game. The [Game's](game) [Turn Manager](turn-manager) does a POST at this resource to get the state that has to be decided by the worker that runs the users code. 

For example, the **world map** object has a much smaller responsibility then [game's version](world-map), being mostly an utility that allows accessing map characteristics such as cells, the cell content, visibility of a cell, and so on. The idea behind this is that the worker has to handle only **a state of the world** at a time and decide an action for its avatar. 

Another important object is the Avatar State. Opposed to the game's avatar, the avatar seen by the user is only an object that encapsulates the avatar's state:

```python 
class AvatarState(object):
    def __init__(self, location, health, score, events):
        self.location = Location(**location)
        self.health = health
        self.score = score
        self.events = events
```
