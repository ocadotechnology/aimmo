from rest_framework import serializers
from django.http import JsonResponse


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=1)
    settings = serializers.SerializerMethodField("get_settings_as_json")

    def get_settings_as_json(self, game):
        return JsonResponse(game.settings_as_dict())
