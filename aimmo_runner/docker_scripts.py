import docker
import platform
import re
from shell_api import (run_command, create_test_bin, BASE_DIR)
import json
import os


def vm_none_enabled(raw_env_settings):
    """
    Check if the VM driver is enabled or not. This is important to see where the environment variables live.

    :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
    :return: Boolean value indicating if enabled or not.
    """
    return False if 'driver does not support' in raw_env_settings else True


def create_docker_client(raw_env_settings):
    """
    Create a docker client using the python SDK.

    :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
    :return:
    """
    if vm_none_enabled(raw_env_settings):
        matches = re.finditer(r'^export (.+)="(.+)"$', raw_env_settings, re.MULTILINE)
        env_variables = dict([(m.group(1), m.group(2)) for m in matches])

        return docker.from_env(
            environment=env_variables,
            version='auto',
        )
    else:
        # VM driver is set
        return docker.from_env(
            version='auto'
        )


def build_docker_images(minikube=None):
    """
    Find environment settings and builds docker images for each directory.

    :param minikube: Executable command to run in terminal.
    """
    print('Building docker images')
    if minikube:
        raw_env_settings = run_command([minikube, 'docker-env', '--shell="bash"'], True)
        client = create_docker_client(raw_env_settings)
    else:
        client = docker.from_env(version='auto')

    directories = ('aimmo-game', 'aimmo-game-creator', 'aimmo-game-worker')
    for dir in directories:
        path = os.path.join(BASE_DIR, dir)
        tag = 'ocadotechnology/%s:test' % dir
        print("Building %s..." % tag)
        client.images.build(
            path=path,
            tag=tag,
            encoding='gzip'
        )


def delete_containers():
    """Delete any containers starting with 'aimmo'."""
    client = docker.from_env(version='auto')

    containers = [container for container in client.containers.list(all=True) if container.name.startswith('aimmo')]
    for container in containers:
        container.remove(force=True)


def start_game_creator():
    """Start an aimmo-game-creator docker container."""
    os_name = platform.system()
    client = docker.from_env(version='auto')
    template = {
        'detach': True,
        'tty': True,
        'environment': {
            'FLASK_ENV': 'development',
            'WORKER_MANAGER': 'local'
        },
        'volumes': {
            '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}
        }
    }
    if os_name == 'Linux':
        template['environment']['LOCALHOST_IP'] = '127.0.0.1'
        template['network_mode'] = 'host'
    else:
        template['environment']['LOCALHOST_IP'] = 'host.docker.internal'

    template['environment']['CONTAINER_TEMPLATE'] = json.dumps(template)
    kwargs = template.copy()
    client.containers.run(
        name='aimmo-game-creator',
        image='ocadotechnology/aimmo-game-creator:test',
        **kwargs
    )
