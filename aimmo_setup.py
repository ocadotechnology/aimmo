from __future__ import print_function
from enum import Enum
import platform
import subprocess
import traceback

from subprocess import PIPE, CalledProcessError

DEFAULT_HOST_TYPE = "MAC"

valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}


class OSType(Enum):
    MAC = 1
    LINUX = 2
    WINDOWS = 3


def _cmd(command, comment=None):
    """
    Run command inside a terminal

    Args:
        command (str): command to be run
    """
    if comment:
        print((comment + " ").ljust(103, "."), end=" ")

    p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    (stdout, stderr) = p.communicate()

    if p.returncode != 0:
        if comment:
            print("FAIL")
        raise CalledProcessError(p.returncode, command, stdout, stderr)

    if comment:
        print("DONE")


def install_yarn(os_type):
    """
    :param operatingSystem: values from the OStypes dict. (Should be updated to enum once python 3 is available)

    OS dependant, so it must be passed to this function in order to run correctly.
    """
    print("Installing Yarn...")
    if os_type == OSType.MAC:
        _cmd("brew install yarn")
    elif os_type == OSType.LINUX:
        _cmd("sudo apt-get install yarn")


def install_pipenv(os_type):
    """
    :param os_type: values from the OStypes dict. (Should be updated to enum once python 3 is available)

    OS dependant, so it must be passed to this function in order to run correctly.
    """
    print("Installing pipenv...")
    if os_type == OSType.MAC:
        _cmd("brew install pipenv")
    elif os_type == OSType.LINUX:
        _cmd("pip install pipenv")
    elif os_type == OSType.WINDOWS:
        pass
    else:
        raise Exception


def install_docker(os_type):
    """
    :param os_type: values from the OStypes dict. (Should be updated to enum once python 3 is available)

    OS dependant, so it must be passed to this function in order to run correctly.
    """
    print("Installing Docker...")
    if os_type == OSType.MAC:
        _cmd("brew cask install docker")
    elif os_type == OSType.LINUX:
        _cmd("sudo apt-get install docker-ce")
    elif os_type == OSType.WINDOWS:
        pass
    else:
        raise Exception


def install_minikube(os_type):
    """
    :param os_type: values from the OStypes dict. (Should be updated to enum once python 3 is available)

    OS dependant, so it must be passed to this function in order to run correctly.
    """
    print(
        "Installing minikube..."
    )  # If minikube version changes this will need updating
    if os_type == OSType.MAC:
        _cmd(
            "curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-darwin-amd64"
        )
        _cmd("chmod +x minikube")
        _cmd("sudo mv minikube /usr/local/bin/")
    elif os_type == OSType.LINUX:
        _cmd(
            "curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-linux-amd64"
        )
        _cmd("chmod +x minikube")
        _cmd("sudo mv minikube /usr/local/bin/")
    elif os_type == OSType.WINDOWS:
        pass
    else:
        raise Exception


def install_kurbernetes(os_type):
    """
    :param os_type: values from the OStypes dict. (Should be updated to enum once python 3 is available)

    OS dependant, so it must be passed to this function in order to run correctly.
    """
    print(
        "Installing Kubernetes..."
    )  # If kubernetes version changes this will need updating
    if os_type == OSType.MAC:
        _cmd(
            "curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.9.4/bin/darwin/amd64/kubectl"
        )
        _cmd("chmod +x kubectl")
        _cmd("sudo mv kubectl /usr/local/bin/")
    elif os_type == OSType.LINUX:
        _cmd("sudo snap install kubectl --classic")
    elif os_type == OSType.WINDOWS:
        pass
    else:
        raise Exception


def install_pip():  # Linux only
    print("Installing pip...")
    _cmd("sudo apt-get install python-pip")


def install_snap():  # Linux only
    print("Installing snap...")
    _cmd("sudo apt install snapd")


def install_nodejs():  # Linux only
    print("Installing Nodejs...")
    _cmd("sudo apt-get install -y nodejs")


def run_pipenv_install():  # OS independent
    print('Running "pipenv install"...')
    _cmd("pipenv install --dev")


def set_up_frontend_dependencies():  # Mac & Linux only
    print("Setting up frontend dependencies...")
    _cmd("cd ./game_frontend | sudo yarn")


def check_homebrew():  # Mac only
    _cmd("brew -v")
    print("Homebrew Found...")


def check_for_cmdtest():  # Linux/Ubuntu only
    """
    This function is for use within the Linux setup section of the script. It checks if
    the cmdtest package is installed, if it is we ask the user if we can remove it, if yes
    we remove the package, if not the process continues without removing it.
    """
    p = subprocess.Popen(
        "dpkg-query -W -f='${status}' cmdtest", shell=True, stdout=PIPE
    )
    (stdout, _) = p.communicate()
    if "unknown" not in stdout:
        print(
            "Looks like cmdtest is installed on your machine, this can cause issues when installing Yarn."
        )

        answer = False
        answered = False
        while not answered:
            choice = raw_input("Is it okay if I remove cmdtest? [y/n]").lower()
            if choice in valid:
                answer = valid[choice]
                answered = True
            else:
                print("Please answer 'yes' or 'no' ('y' or 'n').")
        if answer:
            print("Removing cmdtest...")
            _cmd("apt-get remove cmdtest")
        else:
            print("Continuing without removing cmdtest...")


def update_apt_get():  # Linux only
    print("Updating apt-get...")
    _cmd("sudo apt-get update")


def get_nodejs():  # Linux only
    print("Getting Nodejs...")
    _cmd("curl python-software-properties | sudo apt-get install")
    _cmd("curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -")


def add_aimmo_to_hosts_file():  # Mac & Linux only
    with open("/etc/hosts", "r") as hostfile:
        data = hostfile.read().replace("\n", "")
    if "192.168.99.100 local.aimmo.codeforlife.education" not in data:
        print("Adding Kurono to /etc/hosts...")
        _cmd(
            "sudo sh -c 'echo 192.168.99.100 local.aimmo.codeforlife.education >> /etc/hosts'"
        )
    else:
        print("Kurono already present in /etc/hosts...")


def add_parcel_bundler():  # Mac & Linux only
    print("Adding parcel-bundler globally...")
    _cmd("yarn global add parcel-bundler")


def configure_yarn_repo():  # Linux only
    print("Configuring Yarn repository...")
    _cmd("curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -")
    _cmd(
        'echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list'
    )


def mac_setup(os_type):
    """
    Runs the list of commands, sequentially, needed in order to set up Kurono for a Mac.
    After this has been run the user needs to open Docker to finalise its install,
    and get the unity package for Kurono from aimmo-unity.
    """
    tasks = [
        ensure_homebrew_installed,
        install_yarn,
        yarn_add_parcel_bundler,
        set_up_frontend_dependencies,
        install_pipenv,
        run_pipenv_install,
        install_docker,
        install_minikube,
        install_kubectl,
    ]

    for task in tasks:
        task(os_type)


def windows_setup(os_type):
    raise NotImplementedError


def linux_setup(os_type):
    tasks = [
        update_apt_packages,
        get_nodejs,
        install_nodejs,
        check_for_cmdtest,
        configure_yarn_repo,
        install_yarn,
        yarn_add_parcel_bundler,
        install_pip,
        install_pipenv,
        set_up_frontend_dependencies,
        install_kubectl,
        install_docker,
        add_aimmo_to_hosts_file,
    ]

    for task in tasks:
        task(os_type)


def get_os_type():
    """
    Return the os type if one can be determined

    Returns:
        OSType: OS type
    """
    system = platform.system()

    system_os_type_map = {
        "Darwin": OSType.MAC,
        "Linux": OSType.LINUX,
        "Windows": OSType.WINDOWS,
    }

    try:
        return system_os_type_map[system]
    except KeyError:
        raise KeyError(str(system))


def setup_factory(os_type):
    """
    Return the setup function which matches supplied host type

    Args:
        os_type (OSType): the type of host to setup

    Returns:
        Callable: setup function
    """
    if os_type == OSType.MAC:
        return mac_setup
    elif os_type == OSType.LINUX:
        return linux_setup
    elif os_type == OSType.WINDOWS:
        return windows_setup

    raise RuntimeError("could not find setup function for OS type")


print(
        "+----------------------------------------------------------------------------------------------------------+\n"
        "| Welcome to Kurono!                                                                                       |\n"
        "| This script should make your life a little easier,                                                       |\n"
        "| just be kind if it doesn't work.                                                                         |\n"
        "| You may be asked to enter your password during this setup.                                               |\n"
        "+----------------------------------------------------------------------------------------------------------+\n"
)

try:
    os_type = get_os_type()
    setup = setup_factory(os_type)
    print("%s found!" % os_type.name)
    try:
        setup(os_type)
    except CalledProcessError as e:
        print("Something has gone wrong.")
        print("Command '%s' returned exit code '%s'" % (e.command, e.returncode))
        traceback.print_exc()
    except OSError as e:
        print("Tried to execute a command that didn't exist.")
        traceback.print_exc()
    except ValueError as e:
        print("Tried to execute a command with invalid arguments.")
        traceback.print_exc()
    except:
        print("An unexpected error has occured during setup:\n")
        raise
except KeyError as e:
    print(
        "System %s is not supported. Maybe you're using\n"
        "something other than Windows, Mac, or Linux?" % e
    )
except:
    print("An unexpected error has occured:\n")
    raise
