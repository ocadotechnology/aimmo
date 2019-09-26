from django.contrib import admin
from models import Avatar, Game


class GameDataAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    readonly_fields = ["players"]

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
