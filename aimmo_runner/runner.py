import django
import logging
import os
import sys
import time
from django.conf import settings
from shell_api import log, run_command, run_command_async
print "GOT HERE, About to import User"
print sys.path
#sys.path.append("/home/travis/build/ocadotechnology/aimmo")

try:
    if os.environ['CI'] == "true":
        print "CI TRUE"
        ROOT_DIR_LOCATION = os.environ['TRAVIS_BUILD_DIR']
    else:
        print "CI NOT TRUE"
        ROOT_DIR_LOCATION = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
except KeyError:
    print "HELLO"
    ROOT_DIR_LOCATION = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
print "HELLO00000"
print ROOT_DIR_LOCATION
_MANAGE_PY = os.path.join(ROOT_DIR_LOCATION, 'example_project', 'manage.py')
_SERVICE_PY = os.path.join(ROOT_DIR_LOCATION, 'aimmo-game-creator', 'service.py')
_FRONTEND_BUNDLER_JS = os.path.join(ROOT_DIR_LOCATION, 'game_frontend', 'djangoBundler.js')

PROCESSES = []


def create_superuser_if_missing(username, password):
    from django.contrib.auth.models import User
    print "About to import user"
    print "imported user"
    try:
        User.objects.get_by_natural_key(username)
        print "try case"
    except User.DoesNotExist:
        print "GOT HERE"
        log('Creating superuser %s with password %s' % (username, password))
        User.objects.create_superuser(username=username, email='admin@admin.com',
                                      password=password)


def run_something(use_minikube, server_wait=True, capture_output=False, test_env=False):
    logging.basicConfig()
    sys.path.append(os.path.join(ROOT_DIR_LOCATION, 'example_project'))
    if os.environ['DJANGO_SETTINGS_MODULE'] is None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")
    django.setup()
    print "GETTING ENV"
    run_command(['pip', 'install', '-e', ROOT_DIR_LOCATION], capture_output=capture_output)
    if not test_env:
        run_command(['python', _MANAGE_PY, 'migrate', '--noinput'], capture_output=capture_output)
    run_command(['python', _MANAGE_PY, 'collectstatic', '--noinput'], capture_output=capture_output)

    create_superuser_if_missing(username='admin', password='admin')

    server_args = []
    if use_minikube:
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(parent_dir, 'aimmo_runner'))

        os.chdir(ROOT_DIR_LOCATION)
        run_command(['pip', 'install', '-r', os.path.join(ROOT_DIR_LOCATION, 'minikube_requirements.txt')],
                    capture_output=capture_output)

        # Import minikube here, so we can install the deps first
        from aimmo_runner import minikube
        minikube.start()

        server_args.append('0.0.0.0:8000')
        os.environ['AIMMO_MODE'] = 'minikube'
    else:
        time.sleep(2)
        game_testing = run_command_async(['python', _SERVICE_PY, '127.0.0.1', '5000'], capture_output=capture_output)
        PROCESSES.append(game_testing)
        os.environ['AIMMO_MODE'] = 'threads'

    os.environ['NODE_ENV'] = 'development' if settings.DEBUG else 'production'
    server_testing = run_command_async(['python', _MANAGE_PY, 'runserver'] + server_args, capture_output=capture_output)
    frontend_bundler = run_command_async(['node', _FRONTEND_BUNDLER_JS], capture_output=capture_output)
    PROCESSES.append(server_testing)
    PROCESSES.append(frontend_bundler)

    if server_wait is True:
        try:
            game_testing.wait()
        except NameError:
            pass

        server_testing.wait()

    return PROCESSES
