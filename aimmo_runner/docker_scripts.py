from __future__ import absolute_import
from __future__ import print_function

import os
import re

import docker

from .shell_api import BASE_DIR, run_command


def create_docker_client(use_raw_env=False, minikube=None):
    """
    Create a docker client using the python SDK.

    :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
    :return:
    """
    if use_raw_env:
        raw_env_settings = run_command([minikube, "--profile", "agones", "docker-env", '--shell="bash"'], True).decode(
            "utf-8"
        )
        matches = re.finditer(r'^export (.+)="(.+)"$', raw_env_settings, re.MULTILINE)
        env_variables = dict([(m.group(1), m.group(2)) for m in matches])

    else:
        # VM driver is set
        env_variables = os.environ

    env_variables["DOCKER_BUILDKIT"] = "1"
    return docker.from_env(environment=env_variables, version="auto")


def build_docker_images(minikube=None, build_target=None):
    """
    Find environment settings and builds docker images for each directory.

    :param minikube: Executable command to run in terminal.
    """
    print("Building docker images")
    if minikube:
        client = create_docker_client(use_raw_env=True, minikube=minikube)
    else:
        client = create_docker_client(use_raw_env=False, minikube=minikube)

    path = os.path.join(BASE_DIR, "aimmo-game")
    tag = "ocadotechnology/aimmo-game:test"
    print("Building %s..." % tag)
    client.images.build(path=path, tag=tag, encoding="gzip", target=build_target, rm=True)



def delete_containers():
    """Delete any containers starting with 'aimmo'."""
    client = docker.from_env(version="auto")

    containers = [container for container in client.containers.list(all=True) if container.name.startswith("aimmo")]
    for container in containers:
        container.remove(force=True)
