#!/user/bin/env python
import errno
import platform
import os
import re
import socket
import stat
import tarfile
from run import run_command
from urllib import urlretrieve
from urllib2 import urlopen
from zipfile import ZipFile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_BIN = os.path.join(BASE_DIR, 'test-bin')
OS = platform.system().lower()
FILE_SUFFIX = '.exe' if OS == 'windows' else ''
KUBECTL = os.path.join(TEST_BIN, 'kubectl%s' % FILE_SUFFIX)
MINIKUBE = os.path.join(TEST_BIN, 'minikube%s' % FILE_SUFFIX)
DOCKER_FOLDER = os.path.join(TEST_BIN, 'docker')
DOCKER = os.path.join(DOCKER_FOLDER, 'docker%s' % FILE_SUFFIX)
CREATOR_YAML = os.path.join(TEST_BIN, 'rc-aimmo-game-creator.yaml')


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


def download_kubectl():
    if os.path.isfile(KUBECTL):
        return
    print('Downloading kubectl')
    version = get_latest_github_version('kubernetes/kubernetes')
    url = 'http://storage.googleapis.com/kubernetes-release/release/%s/bin/%s/amd64/kubectl%s' % (version, OS, FILE_SUFFIX)
    download_exec(url, KUBECTL)


def download_minikube():
    if os.path.isfile(MINIKUBE):
        return
    print('Downloading minikube')
    version = get_latest_github_version('kubernetes/minikube')
    url = 'https://storage.googleapis.com/minikube/releases/%s/minikube-%s-amd64%s' % (version, OS, FILE_SUFFIX)
    download_exec(url, MINIKUBE)


def download_docker():
    if os.path.isfile(DOCKER):
        return
    print('Downloading docker')
    try:
        if OS == 'windows':
            url = 'https://get.docker.com/builds/Windows/x86_64/docker-latest.zip'
            download = ZipFile(urlretrieve(url)[0])
        else:
            url = 'https://get.docker.com/builds/%s/x86_64/docker-latest.tgz' % platform.system()
            download = tarfile.open(urlretrieve(url)[0])
        download.extractall(TEST_BIN)
    finally:
        try:
            download.close()
        except Exception:
            pass
    make_exec(DOCKER)


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


def create_creator_yaml():
    orig_path = os.path.join(BASE_DIR, 'aimmo-game-creator', 'rc-aimmo-game-creator.yaml')
    with open(orig_path) as orig_file:
        orig_content = orig_file.read()
    new_content = orig_content.replace('latest', 'test').replace('https://staging-dot-decent-digit-629.appspot.com/aimmo', 'http://%s:8000/players' % get_ip())
    with open(CREATOR_YAML, 'w') as new_file:
        new_file.write(new_content)


def start_cluster():
    status = run_command([MINIKUBE, 'status'], True)
    if status.startswith('Running'):
        print('Cluster already running')
    else:
        run_command([MINIKUBE, 'start', '--memory=2048', '--cpus=2'])


def build_docker_images():
    start_cluster()
    print('Building docker images')
    raw_env_settings = run_command([MINIKUBE, 'docker-env', '--shell="bash"'], True)
    matches = re.finditer(r'^export (.+)="(.+)"$', raw_env_settings, re.MULTILINE)
    for match in matches:
        name = match.group(1)
        value = match.group(2)
        os.environ[name] = value
    dirs = ('aimmo-game', 'aimmo-game-creator', 'aimmo-game-worker')
    for dir in dirs:
        path = os.path.join(BASE_DIR, dir)
        run_command([DOCKER, 'build', '-t', 'ocadotechnology/%s:test' % dir, path])


def restart_pods():
    print('Restarting pods')
    run_command([KUBECTL, 'delete', 'rc', '--all'])
    run_command([KUBECTL, 'delete', 'pods', '--all'])
    run_command([KUBECTL, 'delete', 'service', '--all'])
    run_command([KUBECTL, 'create', '-f', CREATOR_YAML])


def start():
    if platform.machine().lower() not in ('amd64', 'x86_64'):
        raise ValueError('Requires 64-bit')
    create_test_bin()
    download_kubectl()
    download_minikube()
    download_docker()
    create_creator_yaml()
    start_cluster()
    build_docker_images()
    restart_pods()
    print('Cluster ready')
