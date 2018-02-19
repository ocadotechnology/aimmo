#!/user/bin/env python
from __future__ import print_function

import docker
import kubernetes
import os
import re
import socket
import yaml
import platform
from shell_api import (run_command, create_test_bin, BASE_DIR)

MINIKUBE_EXECUTABLE = "minikube"


def get_ip():
    # http://stackoverflow.com/a/28950776/671626
    os_name = platform.system()
    if os_name == "Darwin":
        return socket.gethostbyname(socket.gethostname())

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def restart_ingress_addon(minikube):
    try:
        run_command([minikube, 'addons', 'disable', 'ingress'])
    except:
        pass
    run_command([minikube, 'addons', 'enable', 'ingress'])


def create_ingress_yaml():
    path = os.path.join(BASE_DIR, 'ingress.yaml')
    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
    return content


def create_creator_yaml():
    orig_path = os.path.join(BASE_DIR, 'aimmo-game-creator', 'rc-aimmo-game-creator.yaml')
    with open(orig_path) as orig_file:
        content = yaml.safe_load(orig_file.read().replace('latest', 'test').replace('REPLACE_ME', 'http://%s:8000/players' % get_ip()))
    return content


def start_cluster(minikube):
    status = run_command([minikube, 'status'], True)
    if 'minikube: Running' in status:
        print('Cluster already running')
    else:
        run_command([minikube, 'start', '--memory=2048', '--cpus=2'])


def build_docker_images(minikube):
    print('Building docker images')
    raw_env_settings = run_command([minikube, 'docker-env', '--shell="bash"'], True)
    matches = re.finditer(r'^export (.+)="(.+)"$', raw_env_settings, re.MULTILINE)
    env = dict([(m.group(1), m.group(2)) for m in matches])

    client = docker.from_env(
        environment=env,
        version='auto',
    )

    dirs = ('aimmo-game', 'aimmo-game-creator', 'aimmo-game-worker')
    for dir in dirs:
        path = os.path.join(BASE_DIR, dir)
        tag = 'ocadotechnology/%s:test' % dir
        print("Building %s..." % tag)
        client.images.build(
            path=path,
            tag=tag,
            encoding='gzip'
        )


def restart_pods(game_creator, ingress_yaml):
    print('Restarting pods')
    kubernetes.config.load_kube_config(context='minikube')
    api_instance = kubernetes.client.CoreV1Api()
    extensions_api_instance = kubernetes.client.ExtensionsV1beta1Api()
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

    extensions_api_instance.create_namespaced_ingress("default", ingress_yaml)
    api_instance.create_namespaced_replication_controller(
        body=game_creator,
        namespace='default',
    )


def start():
    if platform.machine().lower() not in ('amd64', 'x86_64'):
        raise ValueError('Requires 64-bit')
    create_test_bin()
    os.environ['MINIKUBE_PATH'] = MINIKUBE_EXECUTABLE
    start_cluster(MINIKUBE_EXECUTABLE)
    build_docker_images(MINIKUBE_EXECUTABLE)
    restart_ingress_addon(MINIKUBE_EXECUTABLE)
    ingress = create_ingress_yaml()
    game_creator = create_creator_yaml()
    restart_pods(game_creator, ingress)
    print('Cluster ready')
