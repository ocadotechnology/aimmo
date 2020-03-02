import errno
import os
import platform
import stat
import subprocess
import sys
from subprocess import CalledProcessError

try:
    from urllib.request import urlretrieve, urlopen
except ImportError:
    from urllib import urlretrieve, urlopen

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
TEST_BIN = os.path.join(BASE_DIR, "test-bin")
OS = platform.system().lower()
FILE_SUFFIX = ".exe" if OS == "windows" else ""
KUBECTL = os.path.join(TEST_BIN, "kubectl%s" % FILE_SUFFIX)
MINIKUBE = os.path.join(TEST_BIN, "minikube%s" % FILE_SUFFIX)
FNULL = open(os.devnull, "w")


def log(message):
    sys.stderr.write(message + "\n")


def run_command(args, capture_output=False):
    try:
        if capture_output:
            return subprocess.check_output(args)
        else:
            subprocess.check_call(args)
    except CalledProcessError as e:
        log("Command failed with exit status %d: %s" % (e.returncode, " ".join(args)))
        raise


def run_command_async(args, capture_output=False):
    if capture_output is True:
        p = subprocess.Popen(args, stdout=FNULL, stderr=subprocess.STDOUT)
    else:
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
    result = urlopen("https://github.com/%s/releases/latest" % repo)
    return result.geturl().split("/")[-1]
