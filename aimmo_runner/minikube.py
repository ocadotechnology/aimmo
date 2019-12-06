#!/user/bin/env python
from __future__ import absolute_import
from __future__ import print_function

import os
import platform
import socket
import time
from subprocess import CalledProcessError

import kubernetes
import yaml

from .docker_scripts import build_docker_images
from .shell_api import BASE_DIR, create_test_bin, run_command

MINIKUBE_EXECUTABLE = "minikube"
TIME_FOR_COMPONENTS_TO_DELETE = 5


def get_ip():
    """
    Get a single primary IP address. This will not return all IPs in the
    interface. See http://stackoverflow.com/a/28950776/671626
    :return: Integer with the IP of the user.
    """
    os_name = platform.system()
    if os_name == "Darwin":
        return "192.168.99.1"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # noinspection PyBroadException
    try:
        # doesn't even have to be reachable
        client_socket.connect(("10.255.255.255", 0))
        IP = client_socket.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        client_socket.close()
    return IP


def restart_ingress_addon(minikube):
    """
    Ingress needs to be restarted for old paths to be removed at startup.
    :param minikube: Executable minikube installed beforehand.
    """
    try:
        run_command([minikube, "addons", "disable", "ingress"])
    except:
        pass
    run_command([minikube, "addons", "enable", "ingress"])


def create_ingress_yaml():
    """
    Loads a ingress yaml file into a python object.
    """
    path = os.path.join(BASE_DIR, "ingress.yaml")
    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
    return content


def create_creator_yaml():
    """
    Loads a replication controller yaml file into a python object.
    """
    orig_path = os.path.join(
        BASE_DIR, "aimmo-game-creator", "rc-aimmo-game-creator.yaml"
    )
    with open(orig_path) as orig_file:
        content = yaml.safe_load(
            orig_file.read()
            .replace("latest", "test")
            .replace("REPLACE_ME", "http://%s:8000/kurono/api/games/" % get_ip())
        )
    return content


def start_cluster(minikube):
    """
    Starts the cluster unless it has been already started by the user.
    :param minikube: Executable minikube installed beforehand.
    """
    try:
        run_command([minikube, "status"], True)
        print("Cluster already running")
    except CalledProcessError:
        run_command([minikube, "start", "--memory=2048", "--cpus=2"])


def delete_components(api_instance, extensions_api_instance):
    for rc in api_instance.list_namespaced_replication_controller("default").items:
        api_instance.delete_namespaced_replication_controller(
            body=kubernetes.client.V1DeleteOptions(),
            name=rc.metadata.name,
            namespace="default",
            grace_period_seconds=0,
        )
    for pod in api_instance.list_namespaced_pod("default").items:
        api_instance.delete_namespaced_pod(
            body=kubernetes.client.V1DeleteOptions(),
            name=pod.metadata.name,
            namespace="default",
            grace_period_seconds=0,
        )
    for service in api_instance.list_namespaced_service("default").items:
        api_instance.delete_namespaced_service(
            name=service.metadata.name, namespace="default"
        )
    for ingress in extensions_api_instance.list_namespaced_ingress("default").items:
        extensions_api_instance.delete_namespaced_ingress(
            name=ingress.metadata.name,
            namespace="default",
            body=kubernetes.client.V1DeleteOptions(),
        )


def restart_pods(game_creator_yaml, ingress_yaml):
    """
    Disables all the components running in the cluster and starts them again
    with fresh updated state.
    :param game_creator_yaml: Replication controller yaml settings file.
    :param ingress_yaml: Ingress yaml settings file.
    """
    print("Restarting pods")
    kubernetes.config.load_kube_config(context="minikube")
    api_instance = kubernetes.client.CoreV1Api()
    extensions_api_instance = kubernetes.client.ExtensionsV1beta1Api()

    delete_components(api_instance, extensions_api_instance)
    time.sleep(TIME_FOR_COMPONENTS_TO_DELETE)

    extensions_api_instance.create_namespaced_ingress("default", ingress_yaml)
    api_instance.create_namespaced_replication_controller(
        body=game_creator_yaml, namespace="default"
    )


def create_roles():
    """
    Applies the service accounts, roles, and bindings for restricting
    the rights of certain pods and their processses.
    """
    run_command(["kubectl", "apply", "-Rf", "rbac"])


def start(build_target=None):
    """
    The entry point to the minikube class. Sends calls appropriately to set
    up minikube.
    """
    if platform.machine().lower() not in ("amd64", "x86_64"):
        raise ValueError("Requires 64-bit")
    create_test_bin()
    os.environ["MINIKUBE_PATH"] = MINIKUBE_EXECUTABLE
    start_cluster(MINIKUBE_EXECUTABLE)
    create_roles()
    build_docker_images(MINIKUBE_EXECUTABLE, build_target=build_target)
    restart_ingress_addon(MINIKUBE_EXECUTABLE)
    ingress = create_ingress_yaml()
    game_creator = create_creator_yaml()
    restart_pods(game_creator, ingress)
    print("Cluster ready")
