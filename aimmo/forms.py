from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.forms import ModelChoiceField, ModelForm, Select

from aimmo.models import Game
from common.models import Class


class AddGameForm(ModelForm):
    def __init__(self, classes: QuerySet, *args, **kwargs):
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
        ]

    def clean(self):
        game_class: Class = self.cleaned_data.get("game_class")

        if game_class and not Class.objects.filter(pk=game_class.id).exists():
            raise ValidationError("Sorry, an invalid class was entered")

        return self.cleaned_data
