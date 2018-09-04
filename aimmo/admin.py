from django.contrib import admin

from models import Avatar, Game


class GameDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    readonly_fields = ['players']

    def players(self, obj):
        return "\n".join([u.first_name for u in obj.can_play.all()])

admin.site.register(Avatar)
admin.site.register(Game, GameDataAdmin)
