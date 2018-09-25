# Usage
- [Mac setup](#mac-setup)
- [Ubuntu/Debian setup](#ubuntu-setup)
- [Windows setup](#windows-setup)
- [Testing locally](#testing-locally)
- [Useful information](#useful-information)

## Mac setup

This can be done either manually or using the setup script.

#### Install using the setup script:

* Run `python aimmo_setup.py` in the AI:MMO root directory. Then:
* Open Docker to finalise the install process. (This will install the [latest release](https://www.docker.com/get-started))
* Get the latest Unity bundle release from the [aimmo-unity](https://github.com/ocadotechnology/aimmo-unity) repo.
* See [Useful information](#useful-information) for additional details about the script.

#### Install manually:

* First you get the [brew](https://brew.sh/) package manager. Then:
* Follow the instructions at [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to set up the frontend requirements, (you should be in the game_frontend folder for this step).
* Run `brew install pipenv`, followed by `pipenv install`, then `pipenv shell`. This will get and activate the virtualenv we recommend for the project. (more information on [pipenv](https://pipenv.readthedocs.io/en/latest/))

The game should now be set up to run locally (If you ran the setup script, it will have done these next steps for you). If you wish to be able to run the project with [Kubernetes](https://kubernetes.io/) and containers, follow these next steps:

* Install both [Docker](https://www.docker.com/) and [Virtualbox](https://www.virtualbox.org/wiki/Downloads), using: 
	* `brew update && brew cask install docker virtualbox`
* Install a fixed version of Minikube, (current version is 0.25.2, this can be confirmed [here](https://github.com/ocadotechnology/aimmo/blob/b0fd1bf852b1b2630a8546d173798ec9a670c480/.travis.yml#L23)). To get this, run:
	* `curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/`
* To install kubectl (Kubernetes), use:
	* `curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.9.4/bin/darwin/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/`
* Alter your `/etc/hosts` file by adding the following line to the end of the file: `192.168.99.100 local.aimmo.codeforlife.education`. You may need to use sudo for this step as the file is protected.
* Get the latest Unity bundle release from the [aimmo-unity](https://github.com/ocadotechnology/aimmo-unity) repo.

#### To run AI:MMO:

* Ensure you are inside the python virtualenv, `pipenv shell`.
* To run **locally**, use: `python run.py`.
* If you want to run the project with [Kubernetes](https://kubernetes.io/), first run: `minikube start`.
* Now use `python run.py -k` to run the project using the Kubernetes cluster.

## Ubuntu setup

This can be done either manually or using the setup script.

#### Install using the setup script:

* Run `python aimmo_setup.py` in the AI:MMO root directory. Then:
* Get the latest Unity bundle release from the [aimmo-unity](https://github.com/ocadotechnology/aimmo-unity) repo.
* See [Useful information](#useful-information) for additional details about the script.

#### Install manually:

* First run `sudo apt-get update` to save having to do it later in the process.
* Follow the instructions at [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to set up the frontend requirements, (you should be in the `game_frontend` folder for this step).
* Next run `sudo apt-get install python-pip`, followed by `pip install pipenv` to get the [pipenv](https://pipenv.readthedocs.io/en/latest/)) virtual environment.
* Now use `pipenv install` and `pipenv shell` to get the requirements for the project and enter the virtualenv.

The game should now be set up to run locally (If you ran the setup script, it will have done these next steps for you). If you wish to be able to run the project with [Kubernetes](https://kubernetes.io/) and containers, follow these next steps:

* If not already installed follow the [Virtualbox installation instructions](https://www.virtualbox.org/wiki/Downloads).
* Install [Snap](https://snapcraft.io/)) using `sudo apt install snapd`.
* Now run `sudo snap install kubectl --classic` to install kubectl ([Kubernetes](https://kubernetes.io/)).
* To install [Docker](https://www.docker.com/), either use `sudo apt-get install docker-ce` to install a fixed version of the latest release, or follow the Ubuntu install instructions on the [Docker website](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository).
* Alter your `/etc/hosts` file by adding the following line to the end of the file: `192.168.99.100 local.aimmo.codeforlife.education`. You may need to use sudo for this step as the file is protected.
* Get the latest Unity bundle release from the [aimmo-unity](https://github.com/ocadotechnology/aimmo-unity) repo.

#### To run AI:MMO:

* Ensure you are inside the python virtualenv, `pipenv shell`.
* To run **locally**, use: `python run.py`.
* If you want to run the project with [Kubernetes](https://kubernetes.io/), first run: `minikube start`.
* Now use `python run.py -k` to run the project using the Kubernetes cluster.

## Windows setup

#### Install Manually:
	
* Contact a member of the Code for Life team via the [Code for Life contact form](https://www.codeforlife.education/help/#contact).

The game should now be set up to run locally. If you wish to be able to run the project with [Kubernetes](https://kubernetes.io/) and containers, follow these next steps:

* If not already installed follow the [Virtualbox installation instructions](https://www.virtualbox.org/wiki/Downloads).
* Next, [download chocolatey](https://chocolatey.org/) and run `choco install kubernetes-cli`.
* Then follow the [docker installation instructions for Windows](https://docs.docker.com/docker-for-windows/).
* Alter your `/etc/hosts` file by adding the following line to the end of the file: `192.168.99.100 local.aimmo.codeforlife.education`. You may need admin privileges for this step as the file is protected.

#### To run AI:MMO:

* Ensure you are inside the python virtualenv, `pipenv shell`.
* To run **locally**, use: `python run.py`.
* If you want to run the project with [Kubernetes](https://kubernetes.io/), first run: `minikube start`.
* Now use `python run.py -k` to run the project using the Kubernetes cluster.

## Useful information

Here you can find some other useful information regarding the setup or usage of various aspects of the project.

#### Setup script & other setup information.

* It may be the case that the frontend does not load properly upon starting aimmo (when running the script). If this is the case then you may need to follow the [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to resolve this (usually all the packages are there, it just requires you to set them up manually).
* If the script fails when attempting to install Docker, it may be because you have an old version of docker currently installed. To fix this, run: `sudo apt-get remove docker docker-engine docker.io`, then re-run the script.
* If there is an issue when using containers or the virtual enviroment. Then there small chance that VT-x/AMD-x virtualization has not been enabled on your machine. If this is the case the main way to solve this is to enable it through the BIOS settings.

#### Testing locally

* Use `./all_tests.py` to run all the tests (note that this is several pages of output).
* The `--coverage` option will generate coverage data for the tests using `coverage.py`.

#### Interacting with the cluster

*  `kubectl`  and  `minikube`  can be used to interact with the cluster.
* Running either command without any options will give the most useful commands.
* Use `minikube dashboard` to open the [Kubernetes](https://kubernetes.io/) dashboard in your browser.

#### Useful commands

* To create an another admin account:  `python example_project/manage.py createsuperuser`
    * By default, we create an admin account with credentials admin:admin when you start the project.
