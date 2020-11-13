import json

from rest_framework import serializers

from aimmo.models import Game


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    settings = serializers.SerializerMethodField("get_settings_as_dict")
    status = serializers.CharField(max_length=1)
    class_id = serializers.SerializerMethodField()
    worksheet_id = serializers.SerializerMethodField()
    era = serializers.SerializerMethodField("get_worksheet_era")

    def get_class_id(self, game: Game):
        try:
            return str(game.game_class.id)
        except AttributeError:
            return None

    def get_worksheet_id(self, game: Game):
        try:
            return str(game.worksheet.id)
        except AttributeError:
            return "2"

    def get_worksheet_era(self, game: Game):
        try:
            return str(game.worksheet.era)
        except AttributeError:
            return "1"

    def get_settings_as_dict(self, game: Game):
        return json.dumps(game.settings_as_dict(), sort_keys=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
