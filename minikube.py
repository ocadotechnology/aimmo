#!/user/bin/env python
from __future__ import print_function

import docker
import errno
import kubernetes
import platform
import os
import re
import socket
import stat
import tarfile
import yaml
from run import run_command, get_ip
from urllib import urlretrieve
from urllib2 import urlopen
from zipfile import ZipFile

from kubernetes.client.rest import ApiException

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_BIN = os.path.join(BASE_DIR, 'test-bin')
OS = platform.system().lower()
FILE_SUFFIX = '.exe' if OS == 'windows' else ''
KUBECTL = os.path.join(TEST_BIN, 'kubectl%s' % FILE_SUFFIX)
MINIKUBE = os.path.join(TEST_BIN, 'minikube%s' % FILE_SUFFIX)


def create_test_bin():
    try:
        os.makedirs(TEST_BIN)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


def get_latest_github_version(repo):
    result = urlopen('https://github.com/%s/releases/latest' % repo)
    return result.geturl().split('/')[-1]


def download_exec(url, dest):
    dest = urlretrieve(url, dest)[0]
    make_exec(dest)


def make_exec(file):
    current_stat = os.stat(file)
    os.chmod(file, current_stat.st_mode | stat.S_IEXEC)


def binary_exists(filename):
    # Check if binary is callable on our path
    try:
        run_command([filename], True)
        return True
    except OSError:
        return False


def download_kubectl():
    if binary_exists('kubectl'):
        return
    if os.path.isfile(KUBECTL):
        return
    print('Downloading kubectl')
    version = get_latest_github_version('kubernetes/kubernetes')
    url = 'http://storage.googleapis.com/kubernetes-release/release/%s/bin/%s/amd64/kubectl%s' % (version, OS, FILE_SUFFIX)
    download_exec(url, KUBECTL)


def download_minikube():
    # First check for the user's installation. Don't break it if they have one
    if binary_exists('minikube'):
        return 'minikube'

    if os.path.isfile(MINIKUBE):
        return MINIKUBE
    print('Downloading minikube')
    version = get_latest_github_version('kubernetes/minikube')
    url = 'https://storage.googleapis.com/minikube/releases/%s/minikube-%s-amd64%s' % (version, OS, FILE_SUFFIX)
    download_exec(url, MINIKUBE)
    return MINIKUBE

def create_creator_yaml():
    orig_path = os.path.join(BASE_DIR, 'aimmo-game-creator', 'rc-aimmo-game-creator.yaml')
    with open(orig_path) as orig_file:
        content = yaml.safe_load(orig_file.read().replace('latest', 'test').replace('https://staging-dot-decent-digit-629.appspot.com/aimmo', 'http://%s:8000/players' % get_ip()))
    return content

def start_cluster(minikube, driver="virtualbox", stop=False):
    if stop:
        try:
            run_command([minikube, 'stop'])
        except:
            print('Cluster already stopped')
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
        status = client.build(
            decode=True,
            path=dir,
            tag=tag,
        )
        for line in status:
            if 'stream' in line:
                print(line['stream'], end='')


def restart_pods(game_creator):
    print('Restarting pods')
    kubernetes.config.load_kube_config(context='minikube')
    v1_api = kubernetes.client.CoreV1Api()
    for rc in v1_api.list_namespaced_replication_controller('default').items:
        v1_api.delete_namespaced_replication_controller(body=kubernetes.client.V1DeleteOptions(), name=rc.metadata.name, namespace='default')
    for pod in v1_api.list_namespaced_pod('default').items:
        v1_api.delete_namespaced_pod(body=kubernetes.client.V1DeleteOptions(), name=pod.metadata.name, namespace='default')
    for service in v1_api.list_namespaced_service('default').items:
        v1_api.delete_namespaced_service(name=service.metadata.name, namespace='default')

    try:
        v1_api.create_namespaced_replication_controller(
            body=game_creator,
            namespace='default',
        )
    except ApiException as e:
        # TODO: If the replication controller already exists, we do nothing for the moment
        if e.status == 409:
            print("Replication controller already exists.")
        else:
            raise


def start():
    if platform.machine().lower() not in ('amd64', 'x86_64'):
        raise ValueError('Requires 64-bit')
    create_test_bin()
    download_kubectl()
    minikube = download_minikube()
    os.environ['MINIKUBE_PATH'] = minikube
    start_cluster(minikube)
    build_docker_images(minikube)
    game_creator = create_creator_yaml()
    restart_pods(game_creator)
    print('Cluster ready')

if __name__ == "__main__":
    start()
