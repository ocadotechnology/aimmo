import json
from rest_framework import serializers
from django.http import JsonResponse


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=1)
    settings = serializers.SerializerMethodField("get_settings_as_dict")

    def get_settings_as_dict(self, game):
        return json.dumps(game.settings_as_dict())
