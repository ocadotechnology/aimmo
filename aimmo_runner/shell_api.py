import subprocess
import sys
import os
import stat
import errno
import platform
from subprocess import CalledProcessError
from urllib import urlretrieve, urlopen

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
TEST_BIN = os.path.join(BASE_DIR, 'test-bin')
OS = platform.system().lower()
FILE_SUFFIX = '.exe' if OS == 'windows' else ''
KUBECTL = os.path.join(TEST_BIN, 'kubectl%s' % FILE_SUFFIX)
MINIKUBE = os.path.join(TEST_BIN, 'minikube%s' % FILE_SUFFIX)


def log(message):
    sys.stderr.write(message + "\n")


def run_command(args, capture_output=False):
    try:
        if capture_output:
            return subprocess.check_output(args)
        else:
            subprocess.check_call(args)
    except CalledProcessError as e:
        log('Command failed with exit status %d: %s' % (e.returncode, ' '.join(args)))
        raise


def run_command_async(args):
    p = subprocess.Popen(args)
    return p


def create_test_bin():
    try:
        os.makedirs(TEST_BIN)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


def binary_exists(filename):
    # Check if binary is callable on our path
    try:
        run_command([filename], True)
        return True
    except OSError:
        return False


def download_exec(url, dest):
    dest = urlretrieve(url, dest)[0]
    make_exec(dest)


def make_exec(file):
    current_stat = os.stat(file)
    os.chmod(file, current_stat.st_mode | stat.S_IEXEC)


def get_latest_github_version(repo):
    result = urlopen('https://github.com/%s/releases/latest' % repo)
    return result.geturl().split('/')[-1]


# def download_kubectl():
#     if binary_exists('kubectl'):
#         return
#     if os.path.isfile(KUBECTL):
#         return
#     print('Downloading kubectl')
#     version = get_latest_github_version('kubernetes/kubernetes')
#     url = 'http://storage.googleapis.com/kubernetes-release/release/%s/bin/%s/amd64/kubectl%s' % (version, OS,
#                                                                                                   FILE_SUFFIX)
#     download_exec(url, KUBECTL)
#
#
# def download_minikube():
#     # First check for the user's installation. Don't break it if they have one
#     if binary_exists('minikube'):
#         return 'minikube'
#
#     if os.path.isfile(MINIKUBE):
#         return MINIKUBE
#     print('Downloading minikube')
#     version = get_latest_github_version('kubernetes/minikube')
#     url = 'https://storage.googleapis.com/minikube/releases/%s/minikube-%s-amd64%s' % (version, OS, FILE_SUFFIX)
#     download_exec(url, MINIKUBE)
#     return MINIKUBE
