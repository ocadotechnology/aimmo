from google.cloud import container_v1
import os
import kubernetes
import yaml
import requests

# THIS IS A TEMPORARY LOCAL SCRIPT TO DEPLOY INGRESS ON DEV. WHEN AUTOMATIC
# DEPLOYMENT ON APP-ENGINE IS ADDED. THIS CAN BE DELETED.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_ingress_yaml():
    print("printing basedir: ", BASE_DIR)
    path = os.path.join(BASE_DIR, 'dev_ingress.yaml')
    print("printing path: ", path)

    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
    return content


def create_creator_yaml():
    path = os.path.join(BASE_DIR, 'aimmo-game-creator', 'rc-aimmo-game-creator.yaml')
    with open(path) as yaml_file:
        content = yaml.safe_load(yaml_file.read())
    return content


def restart_pods(game_creator, ingress_yaml):
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


client = container_v1.ClusterManagerClient()

# project_id and zone can be found on the GCP UI. Ours are:
project_id = 'decent-digit-629'
zone = 'europe-west1-b'

# Load the default service account. Should be authenticated locally by the above
# login command.
kubernetes.config.load_kube_config()
api_instance = kubernetes.client.CoreV1Api()
extensions_api_instance = kubernetes.client.ExtensionsV1beta1Api()

ingress = create_ingress_yaml()
game_creator_rc = create_creator_yaml()

restart_pods(game_creator_rc, ingress)
