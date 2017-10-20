#!/usr/bin/env python
import logging
import os
import signal
import subprocess
import sys
import time
import traceback
from subprocess import CalledProcessError

_SCRIPT_LOCATION = os.path.abspath(os.path.dirname(__file__))
_MANAGE_PY = os.path.join(_SCRIPT_LOCATION, 'example_project', 'manage.py')
_SERVICE_PY = os.path.join(_SCRIPT_LOCATION, 'aimmo-game-creator', 'service.py')


if __name__ == '__main__':
    logging.basicConfig()
    sys.path.append(os.path.join(_SCRIPT_LOCATION, 'example_project'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")


def log(message):
    print >> sys.stderr, message


def run_command(args, capture_output=False):
    try:
        if capture_output:
            return subprocess.check_output(args)
        else:
            subprocess.check_call(args)
    except CalledProcessError as e:
        log('Command failed with exit status %d: %s' % (e.returncode, ' '.join(args)))
        raise


PROCESSES = []


def run_command_async(args):
    p = subprocess.Popen(args)
    PROCESSES.append(p)
    return p


def create_superuser_if_missing(username, password):
    from django.contrib.auth.models import User
    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        log('Creating superuser %s with password %s' % (username, password))
        User.objects.create_superuser(username=username, email='admin@admin.com', password=password)


def main(use_minikube):

    run_command(['pip', 'install', '-e', _SCRIPT_LOCATION])
    run_command(['python', _MANAGE_PY, 'migrate', '--noinput'])
    run_command(['python', _MANAGE_PY, 'collectstatic', '--noinput'])

    create_superuser_if_missing(username='admin', password='admin')

    server_args = []
    if use_minikube:
        # Import minikube here, so we can install the deps first
        run_command(['pip', 'install', '-r', os.path.join(_SCRIPT_LOCATION, 'minikube_requirements.txt')])
        import minikube

        minikube.start()
        server_args.append('0.0.0.0:8000')
        os.environ['AIMMO_MODE'] = 'minikube'
    else:
        time.sleep(2)
        game = run_command_async(['python', _SERVICE_PY, '127.0.0.1', '5000'])
        os.environ['AIMMO_MODE'] = 'threads'
    server = run_command_async(['python', _MANAGE_PY, 'runserver'] + server_args)

    try:
        game.wait()
    except NameError:
        pass
    server.wait()


if __name__ == '__main__':
    try:
        main('--kube' in sys.argv or '-k' in sys.argv)
    except Exception as err:
        traceback.print_exc()
        raise
    finally:
        os.killpg(0, signal.SIGTERM)
        time.sleep(0.9)
        os.killpg(0, signal.SIGKILL)
