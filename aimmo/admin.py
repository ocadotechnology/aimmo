from __future__ import absolute_import
from django.contrib import admin
from .models import Avatar, Game, User
import uuid

from .views import _create_avatar_for_user

NUMBER_OF_AVATARS_TO_ADD = 10


def create_avatar_for_game(game):
    user = User.objects.create_user(uuid.uuid4())
    user.save()
    _create_avatar_for_user(user, game.id, "random_avatar")
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
    list_display = ["id", "name"]

    readonly_fields = ["players"]

    actions = [add_test_avatars_to_games]

    def players(self, obj):
        return "\n".join([u.first_name for u in obj.can_play.all()])


class AvatarDataAdmin(admin.ModelAdmin):
    list_display = ["id", "owner_name", "game_name"]

    def owner_name(self, obj):
        return obj.owner

    def game_name(self, obj):
        return obj.game


admin.site.register(Game, GameDataAdmin)
admin.site.register(Avatar, AvatarDataAdmin)
