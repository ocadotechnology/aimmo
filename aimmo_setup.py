import os
import platform
import subprocess
import shlex

from subprocess import PIPE, CalledProcessError


# First we find and store the OS we are currently on, 0 if we didn't figure out which one
hostOS = 0
OStypes = {
    "mac": 1,
    "windows": 2,
    "linux": 3
}
valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}


class Result:
    '''
    Blank object used to store the result of a command run by Popen, do not use this
    outside of the setup script.
    '''
    pass


def _cmd(command):
    '''
    :param command: command/subprocess to be run, as a string.

    Takes in a command/subprocess, runs it, then returns an object containing all
    output from the process. DO NOT USE outside of the AI:MMO-setup script, and DO NOT INCLUDE
    in any release build, as this function is able to run bash scripts, and can run commands
    with sudo if specified.
    '''
    result = Result()

    p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    (stdout, stderr) = p.communicate()

    result.exit_code = p.returncode
    result.stdout = stdout
    result.stderr = stderr
    result.command = command

    if p.returncode != 0:
        raise CalledProcessError

    return result


def install_yarn(operatingSystem):
    '''
    :param operatingSystem: values from the OStypes dict. (Should be updated to enum once python 3 is availible)

    OS dependant, so it must be passed to this function in order to run correctly.
    '''
    print('Installing Yarn...')
    if operatingSystem == OStypes['mac']:
        result = _cmd('brew install yarn')
    elif operatingSystem == OStypes['linux']:
        result = _cmd('sudo apt-get install yarn')
    elif operatingSystem == OStypes['windows']:
        pass
    else:
        raise Exception


def install_pipenv(operatingSystem):
    '''
    :param operatingSystem: values from the OStypes dict. (Should be updated to enum once python 3 is availible)

    OS dependant, so it must be passed to this function in order to run correctly.
    '''
    print('Installing pipenv...')
    if operatingSystem == OStypes['mac']:
        result = _cmd('brew install pipenv')
    elif operatingSystem == OStypes['linux']:
        result = _cmd('pip install pipenv')
    elif operatingSystem == OStypes['windows']:
        pass
    else:
        raise Exception


def install_docker(operatingSystem):
    '''
    :param operatingSystem: values from the OStypes dict. (Should be updated to enum once python 3 is availible)

    OS dependant, so it must be passed to this function in order to run correctly.
    '''
    print('Installing Docker...')
    if operatingSystem == OStypes['mac']:
        result = _cmd('brew cask install docker')
    elif operatingSystem == OStypes['linux']:
        result = _cmd('sudo apt-get install docker-ce')
    elif operatingSystem == OStypes['windows']:
        pass
    else:
        raise Exception


def install_virtualbox(operatingSystem):
    '''
    :param operatingSystem: values from the OStypes dict. (Should be updated to enum once python 3 is availible)

    OS dependant, so it must be passed to this function in order to run correctly.
    '''
    print('Installing Virtualbox...')
    if operatingSystem == OStypes['mac']:
        result = _cmd('brew cask install virtualbox')
    elif operatingSystem == OStypes['linux']:
        result = _cmd('sudo apt-get install docker-ce')
    elif operatingSystem == OStypes['windows']:
        pass
    else:
        raise Exception


def install_minikube(operatingSystem):
    '''
    :param operatingSystem: values from the OStypes dict. (Should be updated to enum once python 3 is availible)

    OS dependant, so it must be passed to this function in order to run correctly.
    '''
    print('Installing minikube...')  # If minikube version changes this will need updating
    if operatingSystem == OStypes['mac']:
        result = _cmd('curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-darwin-amd64')
        result = _cmd('chmod +x minikube')
        result = _cmd('sudo mv minikube /usr/local/bin/')
    elif operatingSystem == OStypes['linux']:
        result = _cmd('curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-linux-amd64')
        result = _cmd('chmod +x minikube')
        result = _cmd('sudo mv minikube /usr/local/bin/')
    elif operatingSystem == OStypes['windows']:
        pass
    else:
        raise Exception


def install_kurbernetes(operatingSystem):
    '''
    :param operatingSystem: values from the OStypes dict. (Should be updated to enum once python 3 is availible)

    OS dependant, so it must be passed to this function in order to run correctly.
    '''
    print('Installing Kubernetes...')  # If kubernetes version changes this will need updating
    if operatingSystem == OStypes['mac']:
        result = _cmd('curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.9.4/bin/darwin/amd64/kubectl')
        result = _cmd('chmod +x kubectl')
        result = _cmd('sudo mv kubectl /usr/local/bin/')
    elif operatingSystem == OStypes['linux']:
        result = _cmd('sudo snap install kubectl --classic')
    elif operatingSystem == OStypes['windows']:
        pass
    else:
        raise Exception


def install_pip():  # Linux only
    print('Installing pip...')
    result = _cmd('sudo apt-get install python-pip')


def install_snap():  # Linux only
    print('Installing snap...')
    result = _cmd('sudo apt install snapd')


def install_nodejs():  # Linux only
    print('Installing Nodejs...')
    result = _cmd('sudo apt-get install -y nodejs')


def run_pipenv_install():  # OS inderpendant
    print('Running "pipenv install"...')
    result = _cmd('pipenv install')


def set_up_frontend_dependencies():  # Mac & Linux only
    print('Setting up frontend dependencies...')
    result = _cmd('cd ./game_frontend | yarn')


def check_homebrew():  # Mac only
    result = _cmd('brew -v')
    print('Homebrew Found...')


def check_for_cmdtest():  # Linux/Ubuntu only
    '''
    This function is for use within the linux setup section of the script. It checks if
    the cmdtest package is installed, if it is we ask the user if we can remove it, if yes
    we remove the package, if not the process continues without removing it.
    '''
    p = subprocess.Popen("dpkg-query -W -f='${status}' cmdtest")
    (stdout, _) = p.communicate()
    if 'unknown' not in stdout:
        print('Looks like cmdtest is installed on your machine, this can cause issues when installing Yarn.')

        answer = False
        answered = False
        while not answered:
            choice = raw_input('Is it okay if I remove cmdtest? [y/n]').lower()
            if choice in valid:
                answer = valid[choice]
                answered = True
            else:
                print("Please answer 'yes' or 'no' ('y' or 'n').")
        if answer:
            print('Removing cmdtest...')
            result = _cmd('apt-get remove cmdtest')
        else:
            print('Continuing without removing cmdtest...')


def update_apt_get():  # Linux only
    print('Updating apt-get...')
    result = _cmd('sudo apt-get update')


def get_nodejs():  # Linux only
    print('Getting Nodejs...')
    result = _cmd('curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -')


def add_aimmo_to_hosts_file():  # Mac & Linux only
    with open("/etc/hosts", "r") as hostfile:
        data = hostfile.read().replace('\n', '')
    if "192.168.99.100 local.AI:MMO.codeforlife.education" not in data:
        print('Adding AI:MMO to /etc/hosts...')
        result = _cmd("sudo sh -c 'echo 192.168.99.100 local.aimmo.codeforlife.education >> /etc/hosts'")
    else:
        print('AI:MMO already present in /etc/hosts...')


def add_parcel_bundler():  # Mac & Linux only
    print('Adding parcel-bundler globally...')
    result = _cmd('yarn global add parcel-bundler')


def configure_yarn_repo():  # Linux only
    print('Configuring Yarn repository...')
    result = _cmd('curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -')
    result = _cmd('echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list')


def mac_setup(hostOS):
    '''
    Runs the list of commands, sequencially, needed in order to set up AI:MMO for a mac.
    After this has been run the user needs to open docker to finalize it's install,
    and get the unity package for AI:MMO from AI:MMO-unity.
    '''
    try:
        check_homebrew()
        install_yarn(hostOS)
        add_parcel_bundler()
        set_up_frontend_dependencies()
        install_pipenv(hostOS)
        run_pipenv_install()
        install_docker(hostOS)
        install_virtualbox(hostOS)
        install_minikube(hostOS)
        install_kurbernetes(hostOS)

        print('---------------------------------------------------------------------------------------------------')
        print("| You now need to get the unity package from the AI:MMO-unity repo, place it's contents           |")
        print('| in aimmo/aimmo/static/unity.  (folder may not exist yet)                                        |')
        print('| You may also need to open docker, just to finalize the install                                  |')
        print('---------------------------------------------------------------------------------------------------')
        print('| Everything should now be ready for you to use aimmo! :D                                         |')
        print('---------------------------------------------------------------------------------------------------')

    except CalledProcessError as e:
        print('A command has return an exit code != 0, so something has gone wrong.')
        print(e)
    except OSError as e:
        print("Tried to execute a command that didn't exist.")
        print(e)
    except ValueError as e:
        print('Tried to execute a command with invalid arguments')
        print(e)
    except Exception as e:
        print("Something went very wrong, maybe i couldn't read hosts? otherwise I have no idea what it was D:")
        print(e)


def windows_setup(hostOS):
    pass


def linux_setup(hostOS):
    try:
        update_apt_get()
        get_nodejs()
        install_nodejs()
        check_for_cmdtest()
        configure_yarn_repo()
        install_yarn()
        add_parcel_bundler()
        install_pip()
        install_pipenv(hostOS)
        set_up_frontend_dependencies()
        install_kurbernetes(hostOS)
        install_docker(hostOS)
        add_aimmo_to_hosts_file()

        print('---------------------------------------------------------------------------------------------------')
        print("| You now need to get the unity package from the AI:MMO-unity repo, place it's contents           |")
        print('| in aimmo/aimmo/static/unity  (folder may not exist yet)                                         |')
        print('---------------------------------------------------------------------------------------------------')
        print('| Everything should now be ready for you to use aimmo! :D                                         |')
        print('---------------------------------------------------------------------------------------------------')

    except CalledProcessError as e:
        print('Command returned an exit code != 0, so something has gone wrong.')
        print(e)
    except OSError as e:
        print("Tried to execute a command that didn't exist.")
        print(e)
    except ValueError as e:
        print('Tried to execute a command with invalid arguments')
        print(e)
    except Exception as e:
        print("Something went very wrong, maybe i couldn't read hosts? otherwise I have no idea what it was D:")
        print(e)


print('---------------------------------------------------------------------------------------------------')
print('| Welcome to AI:MMO! This script should make your life alil easier, just be kind if it doesnt work|')
print('| You may be asked to enter your password during this setup                                       |')
print('---------------------------------------------------------------------------------------------------')

if platform.system() == 'Darwin':
    hostOS = OStypes["mac"]
    print('MAC found!')
    mac_setup(hostOS)
elif platform.system() == 'Windows':
    hostOS = OStypes["windows"]
    print('WINDOWS found!')
    windows_setup(hostOS)
elif platform.system() == 'Linux':
    hostOS = OStypes["linux"]
    print('LINUX found!')
    linux_setup(hostOS)
else:
    print("Could not detect operating system. Maybe you're using")
    print('something other than windows, mac, or linux?')
