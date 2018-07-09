from django.forms import ModelForm

from aimmo.models import Game


class AddGameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ['Main', 'owner', 'auth_token', 'completed', 'main_user', 'static_data', 'can_play',
                   'public', 'generator', 'target_num_cells_per_avatar',
                   'target_num_score_locations_per_avatar', 'score_despawn_chance',
                   'target_num_pickups_per_avatar', 'pickup_spawn_chance', 'obstacle_ratio',
                   'start_height', 'start_width'
                   ]
