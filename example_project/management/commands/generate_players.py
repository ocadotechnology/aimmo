import uuid

from django.core.management import BaseCommand
from django.test import RequestFactory
from django.utils.importlib import import_module
from django.conf import settings
from django.contrib.auth.models import User
from players.views import code as code_view


PLAYER_CODE = '''
class Avatar(object):
    def handle_turn(self, avatar_state, world_state):
        from simulation.action import MoveAction
        from simulation import direction
        import random
        from simulation.action import WaitAction

        self.world_state = world_state
        self.avatar_state = avatar_state

        if world_state.get_cell(avatar_state.location).generates_score:
            return WaitAction()

        possible_directions = self.get_possible_directions()
        directions_to_emphasise = [d for d in possible_directions if self.is_towards(d, self.get_closest_score_location())]
        return MoveAction(random.choice(possible_directions + (directions_to_emphasise * 5)))

    def is_towards(self, direction, location):
        if location:
            return self.distance_between(self.avatar_state.location, location) > \
                self.distance_between(self.avatar_state.location + direction, location)
        else:
            return False

    def distance_between(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_closest_score_location(self):
        score_cells = list(self.world_state.score_cells())
        if score_cells:
            return min(score_cells, key=lambda cell: self.distance_between(cell.location, self.avatar_state.location)).location
        else:
            return None

    def get_possible_directions(self):
        from simulation import direction
        directions = (direction.EAST, direction.SOUTH, direction.WEST, direction.NORTH)
        return [d for d in directions if self.world_state.can_move_to(self.avatar_state.location + d)]
'''


class Command(BaseCommand):
    # Show this when the user types help
    help = "Generate users for the game"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.engine = import_module(settings.SESSION_ENGINE)
        self.request_factory = RequestFactory()

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of users to create')

    # A command must define handle()
    def handle(self, *args, **options):
        num_users = options['num_users']

        for _ in xrange(num_users):
            random_string = str(uuid.uuid4())[:8]
            username = 'zombie-%s' % random_string
            password = '123'
            user = self.create_user(username, password)
            self.post_code(user, PLAYER_CODE)

    def create_user(self, username, password):
        user = User.objects.create_superuser(username, 'user@generated.com', password)
        self.stdout.write('Created user %s with password: %s' % (username, password))
        return user

    def post_code(self, user, player_code):
        request = self.request_factory.post('/any_path', data={'code': player_code})
        session_key = None
        request.session = self.engine.SessionStore(session_key)
        request.user = user

        response = code_view(request)
        if response.status_code == 200:
            self.stdout.write('Posted code for player %s' % user)
        else:
            raise Exception('Failed to submit code for player %s' % user)