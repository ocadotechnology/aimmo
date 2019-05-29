from rest_framework import serializers


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=1)
    generator = serializers.CharField(max_length=20)
    obstacle_ratio = serializers.FloatField()
    pickup_spawn_chance = serializers.FloatField()
    score_despawn_chance = serializers.FloatField()
    start_height = serializers.IntegerField()
    start_width = serializers.IntegerField()
    target_num_cells_per_avatar = serializers.FloatField()
    target_num_pickups_per_avatar = serializers.FloatField()
    target_num_score_locations_per_avatar = serializers.FloatField()
