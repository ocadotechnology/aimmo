from enum import Enum
from collections import defaultdict

class MapFeature(Enum):
    HEALTH_POINT = 'health_point'
    SCORE_POINT = 'score_point'
    PICKUP = 'pickup'
    OBSTACLE = 'obstacle'

class WorldUpdate():
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

    def __init__(self):
        self.players = defaultdict(dict)
        self.map_features = defaultdict(dict)

    def world_update_dict(self):
        return {'players' : self.players, 'map_features' : self.map_features}

    # Player updates

    def create_player(self, player_data):
        # Player data: {id, x, y, rotation, health, score, appearance}
        self.players["create"].append(player_data)

    def delete_player(self, player_id):
        # Player id: {id}
        self.players["delete"].append(player_id)

    def update_player(self, player_update):
        # Player_update: {id, x, y, rotation, health, score}
        self.players["update"].append(player_update)

    # Map features updates

    def create_map_feature(self, map_feature, map_feature_data):
        self.map_features[map_feature.value]["create"].append(map_feature_data)

    def delete_map_feature(self, map_feature, map_feature_id):
        self.map_features[map_feature.value]["delete"].append(map_feature_id)