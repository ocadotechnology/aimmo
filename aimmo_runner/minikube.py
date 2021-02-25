#!/user/bin/env python
import atexit
import os
import platform

import kubernetes
import yaml
from kubernetes.client import AppsV1Api
from kubernetes.config import load_kube_config

from .docker_scripts import build_docker_images
from .shell_api import BASE_DIR, run_command

MINIKUBE_EXECUTABLE = "minikube"


def get_ip():
    internal_ip = str(
        run_command(
            "minikube -p agones ssh grep host.minikube.internal /etc/hosts".split(),
            capture_output=True,
        ).split()[0],
        "utf-8",
    )
    return internal_ip


def create_creator_yaml():
    """
    Loads a replication controller yaml file into a python object.
    """
    orig_path = os.path.join(
        BASE_DIR, "aimmo-game-creator", "aimmo-game-creator-deployment.yaml"
    )
    with open(orig_path) as orig_file:
        content = yaml.safe_load(
            orig_file.read().replace(
                "REPLACE_ME", f"http://{get_ip()}:8000/kurono/api/games/"
            )
        )
    return content


def delete_components():
    apps_api_instance = AppsV1Api()
    for rs in apps_api_instance.list_namespaced_deployment("default").items:
        apps_api_instance.delete_namespaced_deployment(
            body=kubernetes.client.V1DeleteOptions(),
            name=rs.metadata.name,
            namespace="default",
            grace_period_seconds=0,
        )
    delete_fleet_on_exit()


def restart_pods(game_creator_yaml):
    """
    Disables all the components running in the cluster and starts them again
    with fresh updated state.
    :param game_creator_yaml: Replication controller yaml settings file.
    """
    print("Restarting pods")

    run_command(["kubectl", "create", "-f", "agones/fleet.yml"])

    apps_api_instance = AppsV1Api()
    apps_api_instance.create_namespaced_deployment(
        body=game_creator_yaml, namespace="default"
    )


def create_roles():
    """
    Applies the service accounts, roles, and bindings for restricting
    the rights of certain pods and their processses.
    """
    run_command(["kubectl", "apply", "-Rf", "rbac"])


def delete_fleet_on_exit():
    print("Exiting")
    print("Deleting aimmo-game fleet")
    run_command(
        [
            "kubectl",
            "delete",
            "fleet",
            "aimmo-game",
            "--ignore-not-found",
        ]
    )


def start(build_target=None):
    """
    The entry point to the minikube class. Sends calls appropriately to set
    up minikube.
    """
    if platform.machine().lower() not in ("amd64", "x86_64"):
        raise ValueError("Requires 64-bit")
    os.environ["MINIKUBE_PATH"] = MINIKUBE_EXECUTABLE

    # We assume the minikube was started with a profile called "agones"
    load_kube_config(context="agones")

    create_roles()
    build_docker_images(MINIKUBE_EXECUTABLE, build_target=build_target)
    game_creator = create_creator_yaml()
    restart_pods(game_creator)
    atexit.register(delete_components)
    print("Cluster ready")
