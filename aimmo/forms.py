from common.models import Class
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.forms import ModelChoiceField, ModelForm, Select

from aimmo.models import Game, Worksheet


class AddGameForm(ModelForm):
    def __init__(self, classes: QuerySet, *args, **kwargs):
        super(AddGameForm, self).__init__(*args, **kwargs)
        self.fields["game_class"].queryset = classes

    game_class = ModelChoiceField(
        queryset=None, widget=Select, label="Class", required=True
    )

    class Meta:
        model = Game
        fields = [
            "game_class",
        ]

    def full_clean(self) -> None:
        super(AddGameForm, self).full_clean()
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e)

    def clean(self):
        game_class: Class = self.cleaned_data.get("game_class")

        if game_class and not Class.objects.filter(pk=game_class.id).exists():
            raise ValidationError("Sorry, an invalid class was entered")

        return self.cleaned_data
