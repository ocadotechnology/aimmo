import docker
import platform
import re
from shell_api import (run_command, create_test_bin, BASE_DIR)
import json
import os


def create_docker_client(use_raw_env=False, minikube=None):
    """
    Create a docker client using the python SDK.

    :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
    :return:
    """
    if use_raw_env:
        raw_env_settings = run_command([minikube, 'docker-env', '--shell="bash"'], True)
        matches = re.finditer(r'^export (.+)="(.+)"$', raw_env_settings, re.MULTILINE)
        env_variables = dict([(m.group(1), m.group(2)) for m in matches])
        
    else:
        # VM driver is set
        env_variables = os.environ

    env_variables['DOCKER_BUILDKIT'] = "1"
    return docker.from_env(
            environment=env_variables,
            version='auto',
            )


def build_docker_images(minikube=None, build_target=None):
    """
    Find environment settings and builds docker images for each directory.

    :param minikube: Executable command to run in terminal.
    """
    print('Building docker images')
    if minikube:
        client = create_docker_client(use_raw_env=True, minikube=minikube)
    else:
        client = create_docker_client(use_raw_env=False, minikube=minikube)

    directories = ('aimmo-game', 'aimmo-game-creator', 'aimmo-game-worker')
    for dir in directories:
        path = os.path.join(BASE_DIR, dir)
        tag = 'ocadotechnology/%s:test' % dir
        print("Building %s..." % tag)
        client.images.build(
            path=path,
            tag=tag,
            encoding='gzip',
            target=build_target
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
