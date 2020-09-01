from aimmo.models import Game
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelChoiceField, Select
from django.db.models.query import QuerySet


class AddGameForm(ModelForm):
    def __init__(self, playable_games, classes: QuerySet, *args, **kwargs):
        self.playable_games = playable_games
        super(AddGameForm, self).__init__(*args, **kwargs)
        self.fields["game_class"].queryset = classes

    game_class = ModelChoiceField(queryset=None, widget=Select, required=True)

    class Meta:
        model = Game
        exclude = [
            "Main",
            "owner",
            "auth_token",
            "completed",
            "main_user",
            "static_data",
            "can_play",
            "public",
            "generator",
            "target_num_cells_per_avatar",
            "target_num_score_locations_per_avatar",
            "score_despawn_chance",
            "target_num_pickups_per_avatar",
            "pickup_spawn_chance",
            "obstacle_ratio",
            "start_height",
            "start_width",
            "status",
            "worksheet",
        ]

    def clean(self):
        name = self.cleaned_data["name"]

        playable_games_names = [
            playable_game.name
            for playable_game in self.playable_games
            if self.playable_games and name
        ]

        if name in playable_games_names:
            raise ValidationError("Sorry, a game with this name already exists.")

        return self.cleaned_data
