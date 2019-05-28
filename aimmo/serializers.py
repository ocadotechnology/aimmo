from rest_framework import serializers


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=1)
    settings = serializers.JSONField()
