from enum import Enum
from collections import defaultdict

class MapFeature(Enum):
    HEALTH_POINT = 'health_point'
    SCORE_POINT = 'score_point'
    PICKUP = 'pickup'
    OBSTACLE = 'obstacle'

class WorldState():
    """
    The world updates class serves as a buffer between the updates generated
    in different parts of the back-end and the data emitted by the socket.

    It contains all the parameters that need to be sent to the client every
    time the world is updated. These are:
        - Player (aka avatars) creation, deletion and update.
        - Changes in map features, i.e. creation and deletion of:
            * Health points.
            * Score points.
            * Pickups.
            * Obstacles.
    """

    def __init__(self, game_state):
        self.game_state = game_state
        self.ready_to_update = False

        self.players = defaultdict(dict)
        self.map_features = defaultdict(dict)
        self.clear_updates()

    def get_updates(self):
        self.refresh()
        updates = {
            'players'      : dict(self.players),
            'map_features' : dict(self.map_features)
        }
        self.clear_updates()

        #print("--------------------------------------------")
        #print(updates)
        return updates

    def clear_updates(self):
        self.players = {
            'update': [],
            'create': [],
            'delete': []
        }
        for map_feature in MapFeature:
            self.map_features[map_feature.value] = {
                'create': [],
                'delete': []
            }

    # Player updates.

    def create_player(self, player_data):
        # Player data: {id, x, y, rotation, health, score, appearance?}
        self.players["create"].append(player_data)

    def delete_player(self, player_id):
        # Player id: {id}
        self.players["delete"].append(player_id)

    def update_player(self, player_update):
        # Player_update: {id, x, y, rotation, health, score}
        self.players["update"].append(player_update)

    # Map features updates.

    def create_map_feature(self, map_feature, map_feature_data):
        self.map_features[map_feature]["create"].append(map_feature_data)

    def delete_map_feature(self, map_feature, map_feature_id):
        self.map_features[map_feature]["delete"].append(map_feature_id)

    # Refresh the world state. Basically gather information from the avatar manager
    # and the world map and organise it.

    def refresh(self):
        def player_dict(avatar):
            return {
                'id'    : avatar.player_id,
                'x'     : avatar.location.x,
                'y'     : avatar.location.y,
                'score' : avatar.score,
                'health': avatar.health
            }

        def map_feature_dict(map_feature):
            return {
                'id' : hash(map_feature),
                'x'  : map_feature.location.x,
                'y'  : map_feature.location.y
            }

        with self.game_state as game_state:
            world = game_state.world_map

            # Refresh players dictionary.

            for player in game_state.avatar_manager.avatars:
                self.update_player(player_dict(player))

            for player in game_state.avatar_manager.avatars_to_create:
                self.create_player(player_dict(player))

            for player in game_state.avatar_manager.avatars_to_delete:
                self.delete_player(player_dict(player))

            # Refresh map features dictionary.

            for cell in world.cells_to_create():

                # Cell is an obstacle.
                if not cell.habitable:
                    self.create_map_feature(MapFeature.OBSTACLE.value, map_feature_dict(cell))
                    cell.created = True

                # Cell is a score point.
                if cell.generates_score:
                    self.create_map_feature(MapFeature.SCORE_POINT.value, map_feature_dict(cell))
                    cell.created = True



# TODO: Implement pickups
"""
def get_pickups_list(world):
    pickups = []
    for cell in world.pickup_cells():
        pickup = cell.pickup.serialise()
        pickup['location'] = (cell.location.x, cell.location.y)
        pickups.append(pickup)
    return pickups
"""
