import os
import uuid

from django.core.management import BaseCommand
from django.test import RequestFactory
from django.utils.importlib import import_module
from django.conf import settings
from django.contrib.auth.models import User
from players.views import code as code_view


def _load_code_file(filename):
    if not filename.endswith('.py'):
        filename = filename + '.py'

    filepath = os.path.join('players/avatar_examples', filename)
    with open(filepath) as f:
        return f.read()


class Command(BaseCommand):
    # Show this when the user types help
    help = "Generate users for the game"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.engine = import_module(settings.SESSION_ENGINE)
        self.request_factory = RequestFactory()

    def add_arguments(self, parser):
        parser.add_argument('--num-users', type=int, required=True,
            help='Number of users to create')
        parser.add_argument('--avatar-code', type=str, required=True,
            help='The code to use for the avatar')


    # A command must define handle()
    def handle(self, *args, **options):
        num_users = options['num_users']
        code_filename = options['avatar_code']
        code = _load_code_file(code_filename)

        for _ in xrange(num_users):
            random_string = str(uuid.uuid4())[:8]
            username = 'zombie-%s' % random_string
            password = '123'
            user = self.create_user(username, password)
            self.post_code(user, code)

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
