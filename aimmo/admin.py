from __future__ import absolute_import

import uuid

from django.contrib import admin

from .models import Avatar, Game, User, Worksheet


class GameDataAdmin(admin.ModelAdmin):
    search_fields = ["id", "name", "owner__username", "owner__email"]
    list_display = ["id", "name", "owner"]
    raw_id_fields = ["owner", "main_user", "can_play", "game_class"]
    readonly_fields = ["players", "auth_token"]

    def players(self, obj):
        players = "\n".join(
            [student.new_user.first_name for student in obj.game_class.students.all()]
        )
        players = players.join(obj.game_class.teacher.new_user.first_name)
        return players


class AvatarDataAdmin(admin.ModelAdmin):
    search_fields = ["owner__username", "owner__email"]
    list_display = ["id", "owner_name", "game_name"]
    raw_id_fields = ["game"]
    readonly_fields = ["owner", "auth_token"]

    def owner_name(self, obj):
        return obj.owner

    def game_name(self, obj):
        return obj.game


class WorksheetDataAdmin(admin.ModelAdmin):
    search_fields = ["id", "name", "era"]
    list_display = ["id", "name", "era"]


admin.site.register(Game, GameDataAdmin)
admin.site.register(Avatar, AvatarDataAdmin)
admin.site.register(Worksheet, WorksheetDataAdmin)
