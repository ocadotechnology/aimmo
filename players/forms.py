from django.forms import ModelForm

from players.models import Game


class AddGameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ['Main', 'owner', 'auth_token', 'completed', 'main_user', 'static_data']
