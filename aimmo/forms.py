from common.models import Class
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.forms import ModelChoiceField, ModelForm, Select

from aimmo.models import Game, Worksheet


class AddGameForm(ModelForm):
    def __init__(self, classes: QuerySet, *args, **kwargs):
        super(AddGameForm, self).__init__(*args, **kwargs)
        self.fields["game_class"].queryset = classes
        self.fields["worksheet"].queryset = Worksheet.objects.all()

    game_class = ModelChoiceField(
        queryset=None, widget=Select, label="Class", required=True
    )
    worksheet = ModelChoiceField(
        queryset=None, widget=Select, label="Challenge", required=True
    )

    class Meta:
        model = Game
        exclude = [
            "Main",
            "name",
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

    def full_clean(self) -> None:
        super(AddGameForm, self).full_clean()
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e)

    def clean(self):
        game_class: Class = self.cleaned_data.get("game_class")
        worksheet: Worksheet = self.cleaned_data.get("worksheet")

        if game_class and not Class.objects.filter(pk=game_class.id).exists():
            raise ValidationError("Sorry, an invalid class was entered")

        if worksheet and not Worksheet.objects.filter(pk=worksheet.id).exists():
            raise ValidationError("Sorry, an invalid challenge was entered")

        return self.cleaned_data
