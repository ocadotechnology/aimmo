from __future__ import print_function
from enum import Enum
import re
import sys
import platform
import subprocess
import traceback
import inspect
from subprocess import PIPE, CalledProcessError

# python2 support
try:
    input = raw_input
except NameError:
    pass


MINIKUBE_VERSION = "latest"
KUBECTL_VERSION = "latest"


class OSType(Enum):
    MAC = 1
    LINUX = 2
    WINDOWS = 3


class ArchType(Enum):
    AMD64 = 1
    ARM64 = 2


def main():
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
        arch_type = get_arch_type()

        setup = setup_factory(os_type, arch_type)

        try:
            print("Starting setup for OS: %s\n" % os_type.name)
            setup(os_type, arch_type)
            print("\nFinished setup.")
        except CalledProcessError as e:
            print("Something has gone wrong.")
            print("Command '%s' returned exit code '%s'" % (e.cmd, e.returncode))
            traceback.print_exc()
        except OSError as e:
            print("Tried to execute a command that didn't exist.")
            traceback.print_exc()
        except ValueError as e:
            print("Tried to execute a command with invalid arguments.")
            traceback.print_exc()
    except KeyError as e:
        print("Setup encountered an error: %s" % e.args[0])
    except:
        print("An unexpected error has occured:\n")
        raise


def get_os_type():
    """
    Return the OS type if one can be determined

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
        raise KeyError("'%s' system is not supported" % system)


def get_arch_type():
    """
    Return the architecture type

    Returns:
        ArchType: architecture type
    """
    arch = platform.machine()

    arch_type_map = {
        "amd64": ArchType.AMD64,
        "x86_64": ArchType.AMD64,
        "arm64": ArchType.ARM64,
    }

    try:
        return arch_type_map[arch]
    except KeyError:
        raise KeyError("'%s' architecture is not supported" % arch)


def setup_factory(os_type, arch_type):
    """
    Return the setup function which matches supplied host type

    Args:
        os_type (OSType): the type of host to setup
        arch_type (ArchType): host architecture type

    Returns:
        Callable: setup function
    """
    if os_type == OSType.MAC:
        return mac_setup

    elif os_type == OSType.LINUX:
        return linux_setup

    elif os_type == OSType.WINDOWS:
        return windows_setup

    raise RuntimeError("could not find setup function for supplied host type")


def mac_setup(os_type, arch_type):
    """
    Runs the commands needed in order to set up Kurono for MAC

    Args:
        os_type (OSType): host OS type
        arch_type (ArchType): host architecture type
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
        install_helm,
        helm_add_agones_repo,
        minikube_start_profile,
        helm_install_aimmo,
    ]

    _create_sudo_timestamp()

    for task in tasks:
        task(os_type, arch_type)


def windows_setup(os_type, arch_type):
    raise NotImplementedError


def linux_setup(os_type, arch_type):
    """
    Runs the commands needed in order to set up Kurono for LINUX

    Args:
        os_type (OSType): host OS type
        arch_type (ArchType): host architecture type
    """
    tasks = [
        update_apt_packages,
        install_nodejs,
        check_for_cmdtest,
        configure_yarn_repo,
        install_yarn,
        yarn_add_parcel_bundler,
        install_pip,
        install_pipenv,
        run_pipenv_install,
        set_up_frontend_dependencies,
        install_docker,
        install_minikube,
        install_kubectl,
        install_helm,
        helm_add_agones_repo,
        minikube_start_profile,
        helm_install_aimmo,
        add_aimmo_to_hosts_file,
    ]

    _create_sudo_timestamp()

    for task in tasks:
        task(os_type, arch_type)


def _create_sudo_timestamp():
    """
    Request sudo access to create timestamp file for duration of setup
    """
    print("\033[1mrequesting_sudo_access\033[0m... ")

    # Request sudo password before task
    subprocess.Popen(
        "sudo true", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True
    ).communicate()
    print("\033[1mrequesting_sudo_access\033[0m... [ \033[92mOK\033[0m ]")


def _cmd(command, comment=None):
    """
    Run command inside a terminal

    Args:
        command (str): command to be run
        comment (str): optional comment

    Returns:
        Tuple[int, List[str]]: return code, stdout lines output
    """
    stdout_lines = []

    if not comment:
        # Set comment to calling function name
        comment = inspect.currentframe().f_back.f_code.co_name

    if comment:
        print(" " * 110, end="\r")
        print("\033[1m%s\033[0m...\n" % comment, end="\r")

    p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

    for line in iter(p.stdout.readline, b""):
        stdout_lines.append(line)
        sys.stdout.write("%s\r" % line.decode("utf-8")[:-1].rstrip())
        sys.stdout.flush()

    # Delete line
    sys.stdout.write("\x1b[2K")
    sys.stdout.write("\x1b[1A")

    p.communicate()

    if p.returncode != 0:
        if comment:
            sys.stdout.write(
                "\033[1m%s\033[0m... [ \033[93mFAILED\033[0m ]\n" % comment
            )
        raise CalledProcessError(p.returncode, command)

    if comment:
        sys.stdout.write("\033[1m%s\033[0m... [ \033[92mOK\033[0m ]\n" % comment)

    return (p.returncode, stdout_lines)


def ensure_homebrew_installed(os_type, arch_type):
    if os_type == OSType.MAC:
        _cmd("brew -v")


def install_yarn(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        try:
            if _cmd("yarn --version ", "check_yarn")[0] == 0:
                return
        except CalledProcessError:
            pass

    if os_type == OSType.MAC:
        _cmd("brew install yarn")
    elif os_type == OSType.LINUX:
        _cmd("sudo apt-get install yarn")


def yarn_add_parcel_bundler(os_type, arch_type):
    if os_type == OSType.MAC:
        _cmd("yarn global add parcel-bundler")


def set_up_frontend_dependencies(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        _cmd("cd ./game_frontend && sudo yarn")


def install_pipenv(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        try:
            if _cmd("pipenv --version", "check_pipenv")[0] == 0:
                return
        except CalledProcessError:
            pass

    if os_type == OSType.MAC:
        _cmd("brew install pipenv")
    elif os_type == OSType.LINUX:
        _cmd("pip install pipenv")
    elif os_type == OSType.WINDOWS:
        pass
    else:
        raise Exception


def run_pipenv_install(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        _cmd("pipenv install --dev")


def install_docker(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        try:
            if _cmd("docker -v", "check_docker")[0] == 0:
                return
        except CalledProcessError:
            pass

    if os_type == OSType.MAC:
        _cmd("brew install --cask docker")
    elif os_type == OSType.LINUX:
        _cmd("sudo apt-get install docker-ce")


def install_minikube(os_type, arch_type, version=MINIKUBE_VERSION):
    comment = "install_minikube"

    if version == "latest":
        rc, lines = _cmd(
            "curl https://api.github.com/repos/kubernetes/minikube/releases/latest | grep tag_name"
        )
        match = re.search(r"(v[0-9\.]+)", lines[0])
        if rc == 0 and match:
            version = match.group(1)

    if os_type in [OSType.MAC, OSType.LINUX]:
        try:
            _, lines = _cmd("minikube version", "check_minikube")
            if version in lines[0]:
                return
        except CalledProcessError:
            pass

    if os_type == OSType.MAC:
        _cmd(
            "curl -Lo minikube https://storage.googleapis.com/minikube/releases/%s/minikube-darwin-%s"
            % (version, arch_type.name.lower()),
            comment + ": download",
        )
    elif os_type == OSType.LINUX:
        _cmd(
            "curl -Lo minikube https://storage.googleapis.com/minikube/releases/%s/minikube-linux-%s"
            % (version, arch_type.name.lower()),
            comment + ": download",
        )

    if os_type in [OSType.MAC, OSType.LINUX]:
        _cmd("chmod +x minikube", comment + ": set permissions")
        _cmd("sudo mv minikube /usr/local/bin/", comment + ": copy binary")


def install_kubectl(os_type, arch_type, version=KUBECTL_VERSION):
    comment = "install_kubectl"

    if version == "latest":
        rc, lines = _cmd("curl -L -s https://dl.k8s.io/release/stable.txt")
        if rc == 0:
            version = lines[0]

    if os_type in [OSType.MAC, OSType.LINUX]:
        try:
            _, lines = _cmd("kubectl version --client --short", "check_kubectl")
            if version in lines[0]:
                return
        except CalledProcessError:
            pass

    if os_type == OSType.MAC:
        _cmd(
            "curl -Lo kubectl https://dl.k8s.io/release/%s/bin/darwin/%s/kubectl"
            % (
                version,
                (arch_type.name).lower(),
            ),
            comment + ": download",
        )

    if os_type == OSType.LINUX:
        _cmd(
            "curl -Lo kubectl https://dl.k8s.io/release/%s/bin/linux/%s/kubectl"
            % (
                version,
                (arch_type.name).lower(),
            ),
            comment + ": download",
        )

    if os_type in [OSType.MAC, OSType.LINUX]:
        _cmd("chmod +x kubectl", comment + ": set permissions")
        _cmd("sudo mv kubectl /usr/local/bin/", comment + ": copy binary")


def install_helm(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        try:
            res = _cmd("helm version > /dev/null", "check_helm")
            if res[0] == 0:
                return
        except CalledProcessError:
            pass

        _cmd(
            "curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash"
        )


def helm_add_agones_repo(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        _cmd(
            "helm repo add agones https://agones.dev/chart/stable && "
            "helm repo update"
        )


def minikube_start_profile(os_type, arch_type):
    if os_type == OSType.MAC:
        _cmd("minikube start -p agones --driver=hyperkit")

    if os_type == OSType.LINUX:
        _cmd("minikube start -p agones")


def helm_install_aimmo(os_type, arch_type):
    if os_type in [OSType.MAC, OSType.LINUX]:
        try:
            if (
                _cmd(
                    "helm status -n agones-system aimmo > /dev/null", "check_helm_aimmo"
                )[0]
                == 0
            ):
                return
        except CalledProcessError:
            pass

        _cmd(
            "minikube profile agones && "
            "helm install aimmo --namespace agones-system --create-namespace agones/agones"
        )


def install_pip(os_type, arch_type):
    if os_type == OSType.LINUX:
        _cmd("sudo apt-get install python-pip")


def install_snap(os_type, arch_type):
    if os_type == OSType.LINUX:
        _cmd("sudo apt install snapd")


def install_nodejs(os_type, arch_type):
    comment = "install_nodejs"
    if os_type == OSType.LINUX:
        try:
            if _cmd("nodejs --version", "check_nodejs")[0] == 0:
                return
        except CalledProcessError:
            pass

        _cmd(
            "curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash - 1> /dev/null",
            comment + ": download",
        )
        _cmd("sudo apt-get install -y nodejs", comment + ": install")


def check_for_cmdtest(os_type, arch_type):
    """
    This function is for use within the Linux setup section of the script. It checks if
    the cmdtest package is installed, if it is we ask the user if we can remove it, if yes
    we remove the package, if not the process continues without removing it.
    """
    if os_type == OSType.LINUX:
        _, output = _cmd("dpkg-query -W -f='${status}' cmdtest")

        if "unknown" not in output:
            print(
                "Looks like cmdtest is installed on your machine, "
                "this can cause issues when installing Yarn."
            )

            while True:
                choice = input("Is it okay if I remove cmdtest? [y/n]").lower()
                if choice in ["y", "yes"]:
                    _cmd("sudo apt-get remove cmdtest", "remove_cmdtest")
                    break
                if choice in ["n", "no"]:
                    print("Continuing without removing cmdtest...")
                    break
                print("Please answer 'yes' or 'no' ('y' or 'n').")


def update_apt_packages(os_type, arch_type):
    if os_type == OSType.LINUX:
        _cmd("sudo apt-get update")


def add_aimmo_to_hosts_file(os_type, arch_type):
    comment = "add_kurono_to_local_hosts"
    if os_type in [OSType.MAC, OSType.LINUX]:
        with open("/etc/hosts", "r") as hostfile:
            data = hostfile.read().replace("\n", "")
        if "192.168.99.100 local.aimmo.codeforlife.education" not in data:
            _cmd(
                "sudo sh -c 'echo 192.168.99.100 local.aimmo.codeforlife.education >> /etc/hosts'",
                comment,
            )
        else:
            _cmd("true")


def configure_yarn_repo(os_type, arch_type):
    comment = "configure_yarn"
    _cmd(
        "curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -",
        comment + ": add key",
    )
    _cmd(
        'echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list',
        comment + ": add repo",
    )


if __name__ == "__main__":
    main()
