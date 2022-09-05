from __future__ import absolute_import

import logging
import os

import django
import sys
from django.conf import settings

from .shell_api import log, run_command, run_command_async

ROOT_DIR_LOCATION = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))

_MANAGE_PY = os.path.join(ROOT_DIR_LOCATION, "example_project", "manage.py")
_FRONTEND_BUNDLER_JS = os.path.join(ROOT_DIR_LOCATION, "game_frontend", "djangoBundler.js")

PROCESSES = []


def create_superuser_if_missing(username, password):
    from django.contrib.auth.models import User

    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        log("Creating superuser %s with password %s" % (username, password))
        User.objects.create_superuser(username=username, email="admin@admin.com", password=password)


def build_worker_package():
    run_command([os.path.join(ROOT_DIR_LOCATION, "aimmo_runner", "build_worker_wheel.sh")], capture_output=True)


def build_frontend(using_cypress, capture_output):
    if using_cypress:
        run_command(["node", _FRONTEND_BUNDLER_JS], capture_output=capture_output)
    else:
        frontend_bundler = run_command_async(["node", _FRONTEND_BUNDLER_JS], capture_output=capture_output)
        PROCESSES.append(frontend_bundler)


def start_game_servers(build_target, server_args):
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(parent_dir, "aimmo_runner"))
    os.chdir(ROOT_DIR_LOCATION)

    # Import minikube here, so we can install the dependencies first
    from aimmo_runner import minikube

    minikube.start(build_target=build_target)

    server_args.append("0.0.0.0:8000")
    os.environ["AIMMO_MODE"] = "minikube"


def run(server_wait=True, using_cypress=False, capture_output=False, test_env=False, build_target=None):
    logging.basicConfig()

    build_worker_package()

    if test_env:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
    else:
        sys.path.insert(0, os.path.join(ROOT_DIR_LOCATION, "example_project"))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

    django.setup()

    if using_cypress:
        settings.DEBUG = False
        os.environ["LOAD_KUBE_CONFIG"] = "0"

    os.environ["NODE_ENV"] = "development" if settings.DEBUG else "production"

    build_frontend(using_cypress, capture_output)

    run_command(["pip", "install", "-e", ROOT_DIR_LOCATION], capture_output=capture_output)

    if not test_env:
        run_command(["python", _MANAGE_PY, "migrate", "--noinput"], capture_output=capture_output)
        run_command(["python", _MANAGE_PY, "collectstatic", "--noinput", "--clear"], capture_output=capture_output)

    server_args = []
    if not using_cypress:
        start_game_servers(build_target, server_args)

    os.environ["SERVER_ENV"] = "local"
    server = run_command_async(["python", _MANAGE_PY, "runserver"] + server_args, capture_output=capture_output)
    PROCESSES.append(server)

    if server_wait:
        try:
            game.wait()
        except NameError:
            pass

        server.wait()

    return PROCESSES
