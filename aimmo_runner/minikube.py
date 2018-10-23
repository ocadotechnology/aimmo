#!/user/bin/env python
from __future__ import print_function

from subprocess import CalledProcessError

import docker
import kubernetes
import os
import re
import platform
import yaml
import socket
from shell_api import (run_command, create_test_bin, BASE_DIR)
import json

MINIKUBE_EXECUTABLE = "minikube"


def get_ip():
    """
    Get a single primary IP address. This will not return all IPs in the
    interface. See http://stackoverflow.com/a/28950776/671626
    :return: Integer with the IP of the user.
    """
    os_name = platform.system()
    if os_name == "Darwin":
        return socket.gethostbyname(socket.gethostname())

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # noinspection PyBroadException
    try:
        # doesn't even have to be reachable
        client_socket.connect(('10.255.255.255', 0))
        IP = client_socket.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        client_socket.close()
    return IP


def restart_ingress_addon(minikube):
    """
    Ingress needs to be restarted for old paths to be removed at startup.
    :param minikube: Executable minikube installed beforehand.
    """
    try:
        run_command([minikube, 'addons', 'disable', 'ingress'])
    except:
        pass
    run_command([minikube, 'addons', 'enable', 'ingress'])


def create_ingress_yaml():
    """
    Loads a ingress yaml file into a python object.
    """
    path = os.path.join(BASE_DIR, 'ingress.yaml')
    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
    return content


def create_creator_yaml():
    """
    Loads a replication controller yaml file into a python object.
    """
    orig_path = os.path.join(BASE_DIR, 'aimmo-game-creator', 'rc-aimmo-game-creator.yaml')
    with open(orig_path) as orig_file:
        content = yaml.safe_load(orig_file.read().replace('latest', 'test').replace('REPLACE_ME', 'http://%s:8000/aimmo/api/games/' % get_ip()))
    return content


def start_cluster(minikube):
    """
    Starts the cluster unless it has been already started by the user.
    :param minikube: Executable minikube installed beforehand.
    """
    try:
        run_command([minikube, 'status'], True)
        print('Cluster already running')
    except CalledProcessError:
        run_command([minikube, 'start', '--memory=2048', '--cpus=2'])


def create_docker_client(raw_env_settings):
    """
    Creates a docker client using the python SDK.
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


def vm_none_enabled(raw_env_settings):
    """
    Check if the VM driver is enabled or not. This is important to see where
    the environment variables live.
    :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
    :return: Boolean value indicating if enabled or not.
    """
    return False if 'driver does not support' in raw_env_settings else True


def build_docker_images(minikube=None):
    """
    Finds environment settings and builds docker images for each directory.
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
    client = docker.from_env(version='auto')

    containers = [container for container in client.containers.list() if container.name.startswith('aimmo')]
    for container in containers:
        container.remove(force=True)

def start_game_creator():
    client = docker.from_env(version='auto')
    client.containers.run(
        name='aimmo-game-creator',
        image='ocadotechnology/aimmo-game-creator:test',
        detach=True,
        tty=True,
        publish_all_ports=True,
        volumes={
            '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}
        })

def delete_components(api_instance, extensions_api_instance):
    for rc in api_instance.list_namespaced_replication_controller('default').items:
        api_instance.delete_namespaced_replication_controller(
            body=kubernetes.client.V1DeleteOptions(),
            name=rc.metadata.name,
            namespace='default')
    for pod in api_instance.list_namespaced_pod('default').items:
        api_instance.delete_namespaced_pod(
            body=kubernetes.client.V1DeleteOptions(),
            name=pod.metadata.name,
            namespace='default')
    for service in api_instance.list_namespaced_service('default').items:
        api_instance.delete_namespaced_service(
            name=service.metadata.name,
            namespace='default')
    for ingress in extensions_api_instance.list_namespaced_ingress('default').items:
        extensions_api_instance.delete_namespaced_ingress(
            name=ingress.metadata.name,
            namespace='default',
            body=kubernetes.client.V1DeleteOptions())


def restart_pods(game_creator_yaml, ingress_yaml):
    """
    Disables all the components running in the cluster and starts them again
    with fresh updated state.
    :param game_creator_yaml: Replication controller yaml settings file.
    :param ingress_yaml: Ingress yaml settings file.
    """
    print('Restarting pods')
    kubernetes.config.load_kube_config(context='minikube')
    api_instance = kubernetes.client.CoreV1Api()
    extensions_api_instance = kubernetes.client.ExtensionsV1beta1Api()

    delete_components(api_instance, extensions_api_instance)

    extensions_api_instance.create_namespaced_ingress("default", ingress_yaml)
    api_instance.create_namespaced_replication_controller(
        body=game_creator_yaml,
        namespace='default',
    )


def create_roles():
    """
    Applies the service accounts, roles, and bindings for restricting
    the rights of certain pods and their processses.
    """
    run_command(['kubectl', 'apply', '-Rf', 'rbac'])


def start():
    """
    The entry point to the minikube class. Sends calls appropriately to set
    up minikube.
    """
    if platform.machine().lower() not in ('amd64', 'x86_64'):
        raise ValueError('Requires 64-bit')
    create_test_bin()
    os.environ['MINIKUBE_PATH'] = MINIKUBE_EXECUTABLE
    start_cluster(MINIKUBE_EXECUTABLE)
    create_roles()
    build_docker_images(MINIKUBE_EXECUTABLE)
    restart_ingress_addon(MINIKUBE_EXECUTABLE)
    ingress = create_ingress_yaml()
    game_creator = create_creator_yaml()
    restart_pods(game_creator, ingress)
    print('Cluster ready')
