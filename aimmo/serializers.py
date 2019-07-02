import json

from django.http import JsonResponse
from rest_framework import serializers


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=1)
    settings = serializers.SerializerMethodField("get_settings_as_dict")

    def get_settings_as_dict(self, game):
        return json.dumps(game.settings_as_dict())

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
