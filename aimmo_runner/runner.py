import logging
import os
import sys
import time
from shell_api import log, run_command, run_command_async

sys.path.append("/home/travis/build/ocadotechnology/aimmo")

try:
    if os.environ['CI'] == "true":
        ROOT_DIR_LOCATION = os.environ['TRAVIS_BUILD_DIR']
    else:
        ROOT_DIR_LOCATION = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
except KeyError:
    ROOT_DIR_LOCATION = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))

_MANAGE_PY = os.path.join(ROOT_DIR_LOCATION, 'example_project', 'manage.py')
_SERVICE_PY = os.path.join(ROOT_DIR_LOCATION, 'aimmo-game-creator', 'service.py')

PROCESSES = []


def create_superuser_if_missing(username, password):
    from django.contrib.auth.models import User
    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        log('Creating superuser %s with password %s' % (username, password))
        User.objects.create_superuser(username=username, email='admin@admin.com',
                                      password=password)


def run(use_minikube, server_wait=True, capture_output=False):
    logging.basicConfig()
    sys.path.append(os.path.join(ROOT_DIR_LOCATION, 'example_project'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

    run_command(['pip', 'install', '-e', ROOT_DIR_LOCATION], capture_output=capture_output)
    run_command(['python', _MANAGE_PY, 'migrate', '--noinput'], capture_output=capture_output)
    run_command(['python', _MANAGE_PY, 'collectstatic', '--noinput'], capture_output=capture_output)

    create_superuser_if_missing(username='admin', password='admin')

    server_args = []
    if use_minikube:
        # Import minikube here, so we can install the deps first
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(parent_dir, 'aimmo_runner'))

        os.chdir(ROOT_DIR_LOCATION)
        run_command(['pip', 'install', '-r', os.path.join(ROOT_DIR_LOCATION, 'minikube_requirements.txt')],
                    capture_output=capture_output)
        from aimmo_runner import minikube
        minikube.start()

        server_args.append('0.0.0.0:8000')
        os.environ['AIMMO_MODE'] = 'minikube'
    else:
        time.sleep(2)
        game = run_command_async(['python', _SERVICE_PY, '127.0.0.1', '5000'], capture_output=capture_output)
        PROCESSES.append(game)
        os.environ['AIMMO_MODE'] = 'threads'

    server = run_command_async(['python', _MANAGE_PY, 'runserver'] + server_args, capture_output=capture_output)
    PROCESSES.append(server)

    if server_wait is True:
        try:
            game.wait()
        except NameError:
            pass

        server.wait()

    return PROCESSES
