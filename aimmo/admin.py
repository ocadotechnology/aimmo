from __future__ import absolute_import

import uuid

from django.contrib import admin

from .game_creator import create_avatar_for_user
from .models import Avatar, Game, User, Worksheet

NUMBER_OF_AVATARS_TO_ADD = 10


def create_avatar_for_game(game):
    user = User.objects.create_user(uuid.uuid4())
    user.save()
    create_avatar_for_user(user, game.id, "random_avatar")
    return user


def add_test_avatars_to_games(game_data_admin, request, queryset):
    for game in queryset:
        users = [create_avatar_for_game(game) for _ in range(NUMBER_OF_AVATARS_TO_ADD)]
        game.can_play.add(*users)
        game.save()


add_test_avatars_to_games.short_description = "Add {} test avatars to selected games".format(
    NUMBER_OF_AVATARS_TO_ADD
)


class GameDataAdmin(admin.ModelAdmin):
    search_fields = ["id", "name", "owner__username", "owner__email"]
    list_display = ["id", "name", "owner"]
    raw_id_fields = ["owner", "main_user", "can_play"]
    readonly_fields = ["players", "auth_token"]
    actions = [add_test_avatars_to_games]

    def players(self, obj):
        return "\n".join([u.first_name for u in obj.can_play.all()])


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
