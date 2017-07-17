from collections import defaultdict

score_locations = {}

class WorldState():
    """ A 'world state' is what the front-end sees. The front-end needs to
        know the players and a general world that is exposed at each moment in
        time.

        * get_update ---> an update is a modification of the world exposed
            via the socket connection
        * get_init ---> get the initial world state
    """

    def __init__(self):
        pass

    def get_update(self):
        pass

    def get_init(self):
        pass


def get_pickups_list(world):
    pickups = []
    for cell in world.pickup_cells():
        pickup = cell.pickup.serialise()
        pickup['location'] = (cell.location.x, cell.location.y)
        pickups.append(pickup)
    return pickups

class UnityWorldState(WorldState):
    def __init__(self, game_state):
        self.game_state = game_state

    def get_update(self):
        def player_dict(avatar):
            return {
                'id': avatar.player_id,
                'x': avatar.location.x,
                'y': avatar.location.y,
                'score': avatar.score
            }

        with self.game_state as game_state:
            world = game_state.world_map
            player_data = {p.player_id: player_dict(p) for p in game_state.avatar_manager.avatars}

            # TODO: need to make a more clear layout of resources: new_players, deleted_players, etc.
            pickups = get_pickups_list(world)
            ans_dict = {
                'players': player_data,
                'new_players': {},
                'deleted_players': {}
                # 'pickups': pickups # pickups not supported yet
            }
            print ans_dict
            return ans_dict

    def get_init(self):
        with self.game_state as game_state:
            world = game_state.world_map

            # TODO: warn -- we might want new_players, deleted_players in initial dict as well
            curr_dict = defaultdict(dict)
            curr_dict["players"] = self.get_update()["players"]

            map_dimensions = {
                'minX': world.min_x(),
                'minY': world.min_y(),
                'maxX': world.max_x(),
                'maxY': world.max_y()
            }
            curr_dict.update(map_dimensions)

            # for the moment the front-end supports only obstacles
            # we use a hash of the location as an ID for the cells at the moment
            obstacles = []
            for cell in world.all_cells():
                if not cell.habitable:
                    obstacles.append({
                        'id' : hash(cell),
                        'x' : cell.location.x,
                        'y' : cell.location.y
                    })
            curr_dict['objects'] = obstacles

            curr_dict['score_locations'] = [{'x' : cell.location.x, 'y' : cell.location.y} for cell in world.score_cells()]

            return curr_dict