import os
import platform
import subprocess
import shlex

from subprocess import PIPE, CalledProcessError


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
    output from the process. DO NOT USE outside of the aimmo-setup script, and DO NOT INCLUDE
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
        print('extcde: [%s]' % p.returncode)
        print('stderr: [%s]' % stderr)
        print('stdout: [%s]' % stdout)
        raise CalledProcessError

    return result


# First we find and store the OS we are currently on, 0 if we didn't figure it out
# Although if you're not using one the options above for development what are you doing with your life.
hostOS = 0
OStypes = {
    "mac": 1,
    "windows": 2,
    "linux": 3
}
valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

print('---------------------------------------------------------------------------------------------------')
print('| Welcome to aimmo! This script should make your life alil easier, just be kind if it doesnt work |')
print('| You may be asked to enter your password during this setup                                       |')
print('---------------------------------------------------------------------------------------------------')

if platform.system() == 'Darwin':
    hostOS = OStypes["mac"]
    print('MAC found!')
elif platform.system() == 'Windows':
    hostOS = OStypes["windows"]
    print('WINDOWS found!')
elif platform.system() == 'Linux':
    hostOS = OStypes["linux"]
    print('LINUX found!')

if hostOS == OStypes["mac"]:
    """
    This executes the sequence of shell commands needed in order to set up aimmo. At present if changes are made
    to the setup process or versions (such as minikube version) changes, then it will need to be updated manually.
    In future it would be nice to have it automatically find the version we need at the time.

    It would also be nice to implement the ability to automate getting the unity package, however this will require
    selenium and a good amount of thought put into it.

    Note needs homebrew pre-installed in order to run, will let the user know if they don't have it.
    """
    try:
        result = _cmd('brew -v')
        print('Homebrew Found...')

        print('Installing Yarn...')
        result = _cmd('brew install yarn')

        print('Adding parcel-bundler globally...')
        result = _cmd('yarn global add parcel-bundler')

        print('Installing pipenv...')
        result = _cmd('brew install pipenv')

        print('Running "pipenv install"...')
        result = _cmd('pipenv install')

        print('Installing Docker...')
        result = _cmd('brew cask install docker')

        print('Installing Virtualbox...')
        result = _cmd('brew cask install virtualbox')

        print('Setting up frontend dependencies...')
        result = _cmd('cd ./game_frontend | yarn')

        print('Installing minikube...')  # If minikube version changes this will need updating
        result = _cmd('curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-darwin-amd64')
        result = _cmd('chmod +x minikube')
        result = _cmd('sudo mv minikube /usr/local/bin/')

        print('Installing Kubernetes...')  # If kubernetes version changes this will need updating
        result = _cmd('curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.9.4/bin/darwin/amd64/kubectl')
        result = _cmd('chmod +x kubectl')
        result = _cmd('sudo mv kubectl /usr/local/bin/')

        with open("/etc/hosts", "r") as hostfile:
            data = hostfile.read().replace('\n', '')
        if "192.168.99.100 local.aimmo.codeforlife.education" not in data:
            print('Adding aimmo to /etc/hosts...')
            result = _cmd("sudo sh -c 'echo 192.168.99.100 local.aimmo.codeforlife.education >> /etc/hosts'")
        else:
            print('Aimmo already present in /etc/hosts...')

        print('---------------------------------------------------------------------------------------------------')
        print('| You now need to get the unity package from the aimmo-unity repo, place it in aimmo/static/unity |')
        print('| Also, just open up docker to finalize the install for it, then you can run aimmo.               |')
        print('---------------------------------------------------------------------------------------------------')

    except CalledProcessError as e:
        print('A command has return an exit code != 0, so something has gone wrong.')
    except OSError as e:
        print("Tried to execute a command that didn't exist.")
        print(result.stderr)
    except ValueError as e:
        print('Tried to execute a command with invalid arguments')
        print(result.stderr)
    except Exception as e:
        print('Something went very wrong and i have no idea what it was D:')
        print(result.stderr)
elif hostOS == OStypes["windows"]:
    pass
elif hostOS == OStypes["linux"]:
    try:
        print('Updating apt-get...')
        result = _cmd('sudo apt-get update')

        print('Getting Nodejs...')
        result = _cmd('curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -')

        print('Installing Nodejs...')
        result = _cmd('sudo apt-get install -y nodejs')

        # Here we check if cmd test is installed, if it is we ask the user if it's okay to remove it if we find it.
        # If ok, we remove it, if not, we attempt to continue the process without removing.
        # This step has to be done manually as dpkq-query returns a none 0 exit code if it can't find the package.
        # This means within our cmd function it would raise a CalledProcessError causing the code to fail.
        p = subprocess.Popen("dpkg-query -W -f='${status}' cmdtest")
        (stdout, stderr) = p.communicate()
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

        print('Configuring Yarn repository...')
        result = _cmd('curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -')
        result = _cmd('echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list')

        print('Installing Yarn...')
        result = _cmd('sudo apt-get install yarn')

        print('Adding parcel-bundler globally...')
        result = _cmd('yarn global add parcel-bundler')

        print('Installing pip...')
        result = _cmd('sudo apt-get install python-pip')

        print('Installing pipenv...')
        result = _cmd('pip install pipenv')

        print('Installing snap...')
        result = _cmd('sudo apt install snapd')

        print('Installing kubernetes...')
        result = _cmd('sudo snap install kubectl --classic')

        # Installs the latest version of docker, this is a fixed version though.
        print('Installing Docker...')
        result = _cmd('sudo apt-get install docker-ce')

        with open("/etc/hosts", "r") as hostfile:
            data = hostfile.read().replace('\n', '')
        if "192.168.99.100 local.aimmo.codeforlife.education" not in data:
            print('adding aimmo to /etc/hosts...')
            result = _cmd("sudo sh -c 'echo 192.168.99.100 local.aimmo.codeforlife.education >> /etc/hosts'")
        else:
            print('Aimmo already present in /etc/hosts...')

    except CalledProcessError as e:
        print('Command returned an exit code != 0, so something has gone wrong.')
        print(result.stderr)
    except OSError as e:
        print("Tried to execute a command that didn't exist.")
        print(result.stderr)
    except ValueError as e:
        print('Tried to execute a command with invalid arguments')
        print(result.stderr)
    except Exception as e:
        print('Something went very wrong and I have no idea what it was D:')
        print(result.stderr)
else:
    print("Could not detect operating system/ it looks like you're using")
    print('Something other then windows, mac, or linux. Y u do dis?')
