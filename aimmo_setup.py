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

def _cmd(command):
    """
    :param command: command/subprocess to be run, as a string.

    Takes in a command/subprocess, and runs it as if you would
    inside a terminal. DO NOT USE outside of the aimmo-setup script, and DO NOT INCLUDE
    in any release build, as this function is able to run bash scripts, and can run commands
    with sudo if specified.
    """

    p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    (_, _) = p.communicate()

    if p.returncode != 0:
        raise CalledProcessError



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
    try:
        check_homebrew()
        install_yarn(os_type)
        add_parcel_bundler()
        set_up_frontend_dependencies()
        install_pipenv(os_type)
        run_pipenv_install()
        install_docker(os_type)
        install_minikube(os_type)
        install_kurbernetes(os_type)

    except CalledProcessError as e:
        print("A command has return an exit code != 0, so something has gone wrong.")
        traceback.print_exc()
    except OSError as e:
        print("Tried to execute a command that didn't exist.")
        traceback.print_exc()
    except ValueError as e:
        print("Tried to execute a command with invalid arguments.")
        traceback.print_exc()
    except Exception as e:
        print(
            "Something went very wrong, maybe I couldn't read hosts? Otherwise I have no idea what it was D:"
        )
        traceback.print_exc()


def windows_setup(os_type):
    pass


def linux_setup(os_type):
    try:
        update_apt_get()
        get_nodejs()
        install_nodejs()
        check_for_cmdtest()
        configure_yarn_repo()
        install_yarn(os_type)
        add_parcel_bundler()
        install_pip()
        install_pipenv(os_type)
        set_up_frontend_dependencies()
        install_kurbernetes(os_type)
        install_docker(os_type)
        add_aimmo_to_hosts_file()

    except CalledProcessError as e:
        print("Command returned an exit code != 0, so something has gone wrong.")
        traceback.print_exc()
    except OSError as e:
        print("Tried to execute a command that didn't exist.")
        traceback.print_exc()
    except ValueError as e:
        print("Tried to execute a command with invalid arguments")
        traceback.print_exc()
    except Exception as e:
        print(
            "Something went very wrong, maybe I couldn't read hosts? otherwise I have no idea what it was D:"
        )
        traceback.print_exc()


print(
    "---------------------------------------------------------------------------------------------------"
)
print(
    "| Welcome to Kurono! This script should make your life a little easier,                           |"
)
print(
    "| just be kind if it doesn't work.                                                                |"
)
print(
    "| You may be asked to enter your password during this setup.                                      |"
)
print(
    "---------------------------------------------------------------------------------------------------"
)

if platform.system() == "Darwin":
    os_type = OSType.MAC
    print("MAC found!")
    mac_setup(os_type)
elif platform.system() == "Windows":
    os_type = OSType.WINDOWS
    print("WINDOWS found!")
    windows_setup(os_type)
elif platform.system() == "Linux":
    os_type = OSType.LINUX
    print("LINUX found!")
    linux_setup(os_type)
else:
    print("Could not detect operating system. Maybe you're using")
    print("something other than Windows, Mac, or Linux?")
