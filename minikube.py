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
from run import run_command
from urllib import urlretrieve
from urllib2 import urlopen
from zipfile import ZipFile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_BIN = os.path.join(BASE_DIR, 'test-bin')
MANIFESTS = os.path.join(BASE_DIR, 'manifests/')
RENDER_MANIFESTS = os.path.join(BASE_DIR, 'render-manifests.py')
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
        return 'kubectl'
    if os.path.isfile(KUBECTL):
        return KUBECTL
    print('Downloading kubectl...')
    version = get_latest_github_version('kubernetes/kubernetes')
    url = 'http://storage.googleapis.com/kubernetes-release/release/%s/bin/%s/amd64/kubectl%s' % (version, OS, FILE_SUFFIX)
    download_exec(url, KUBECTL)
    return KUBECTL


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


def get_ip():
    # http://stackoverflow.com/a/28950776/671626
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


def render_manifests():
    run_command([RENDER_MANIFESTS, BASE_DIR, 'test', 'http://%s:8000/players/api/games/' % get_ip()])


def start_cluster(minikube):
    status = run_command([minikube, 'status'], True)
    if 'Running' in status:
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

    dirs = ('aimmo-game', 'aimmo-game-creator', 'aimmo-game-worker', 'aimmo-reverse-proxy')
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


def apply_manifests(kubectl):
    print('Applying manifests...')
    run_command([kubectl, '--context=minikube', 'apply', '-f', MANIFESTS])
    print('Deleting existing pods...')
    kubernetes.config.load_kube_config(context='minikube')
    v1_api = kubernetes.client.CoreV1Api()
    for pod in v1_api.list_namespaced_pod('default').items:
        v1_api.delete_namespaced_pod(body=kubernetes.client.V1DeleteOptions(), name=pod.metadata.name, namespace='default')


def start():
    if platform.machine().lower() not in ('amd64', 'x86_64'):
        raise ValueError('Requires 64-bit')
    create_test_bin()
    kubectl = download_kubectl()
    minikube = download_minikube()
    start_cluster(minikube)
    build_docker_images(minikube)
    render_manifests()
    apply_manifests(kubectl)
    os.environ['MINIKUBE_PROXY_URL'] = run_command([minikube, 'service', 'aimmo-reverse-proxy', '--url'], True).strip()
    print('Cluster ready')

if __name__ == "__main__":
    start()
