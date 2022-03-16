from __future__ import absolute_import

from django.contrib import admin

from .models import Avatar, Game


class GameDataAdmin(admin.ModelAdmin):
    search_fields = ["id", "owner__username", "owner__email"]
    list_display = ["id", "owner", "game_class", "school", "worksheet_id", "status"]
    raw_id_fields = ["owner", "main_user", "can_play", "game_class"]
    readonly_fields = ["players", "auth_token"]

    def players(self, obj):
        players = "\n".join(
            [student.new_user.first_name for student in obj.game_class.students.all()]
        )
        players = players.join(obj.game_class.teacher.new_user.first_name)
        return players

    def school(self, obj):
        if obj.game_class:
            return obj.game_class.teacher.school
        else:
            return None


class AvatarDataAdmin(admin.ModelAdmin):
    search_fields = ["owner__username", "owner__email"]
    list_display = ["id", "owner_name", "game_id"]
    raw_id_fields = ["game"]
    readonly_fields = ["owner", "auth_token"]

    def owner_name(self, obj):
        return obj.owner

    def game_id(self, obj):
        return obj.game


admin.site.register(Game, GameDataAdmin)
admin.site.register(Avatar, AvatarDataAdmin)
