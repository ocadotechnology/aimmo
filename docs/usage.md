# Usage

This setup process will allow you to run Kurono locally via [docker](https://www.docker.com/) or a [kubernetes](https://kubernetes.io/) cluster, and to be able to contribute towards the project.

- [Mac setup](#mac-setup)
- [Ubuntu/Debian setup](#ubuntu-setup)
- [Windows setup](#windows-setup)
- [Testing locally](#testing-locally)
- [Useful information](#useful-information)

## Mac setup

This can be done either manually or using the setup script.

#### Install using the setup script:

- Run `python aimmo_setup.py` in the Kurono root directory. Then:
- Open Docker to finalise the install process. (This will install the [latest release](https://www.docker.com/get-started))
- See [Useful information](#useful-information) for additional details about the script.

#### Install manually:

- First you get the [brew](https://brew.sh/) package manager. Then:
- Follow the instructions at [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to set up the frontend requirements, (you should be in the game_frontend folder for this step).
- Follow the instructions for [installing pyenv](https://github.com/pyenv/pyenv#installation).
- Run `brew install pipenv`, followed by `pipenv install --dev` (more information on [pipenv](https://pipenv.readthedocs.io/en/latest/)).
- Install [Docker](https://www.docker.com/): `brew update && brew install --cask docker`.
- Install Minikube: `brew install minikube`.
- Check if you have `kubectl` installed (Kubernetes - it should come with Docker). If not, use: `curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.9.4/bin/darwin/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/`.
- Install helm: `brew install helm`.
- Add agones repo to helm: `helm repo add agones https://agones.dev/chart/stable && helm repo update`.
- Create a minikube profile for agones: `minikube start -p agones --driver=hyperkit`.
- Set the minikube profile to agones: `minikube profile agones`, then install agones using helm: `helm install aimmo --namespace agones-system --create-namespace agones/agones`.

#### To run Kurono:

- Ensure you are inside the python virtualenv, `pipenv shell`.
- First start the agones cluster with: `minikube start -p agones --driver=hyperkit`.
- Now use `python run.py` to run the project.

## Ubuntu setup

This can be done either manually or using the setup script.

#### Install using the setup script:

- Run `python aimmo_setup.py` in the AI:MMO root directory.
- See [Useful information](#useful-information) for additional details about the script.

#### Install manually:

- First run `sudo apt-get update` to save having to do it later in the process.
- Follow the instructions at [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to set up the frontend requirements, (you should be in the `game_frontend` folder for this step).
- Follow the instructions for [installing pyenv](https://github.com/pyenv/pyenv#installation).
- Next run `sudo apt-get install python-pip`, followed by `pip install pipenv` to get the [pipenv](https://pipenv.readthedocs.io/en/latest/)) virtual environment.
- Now use `pipenv install --dev` to get the requirements for the project.
- Install [Snap](https://snapcraft.io/)) using `sudo apt install snapd`.
- Now run `sudo snap install kubectl --classic` to install kubectl ([Kubernetes](https://kubernetes.io/)).
- To install [Docker](https://www.docker.com/), either use `sudo apt-get install docker-ce` to install a fixed version of the latest release, or follow the Ubuntu install instructions on the [Docker website](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository).
- Install Minikube, running `curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64`, then `sudo install minikube-linux-amd64 /usr/local/bin/minikube`
- Install helm: `sudo snap install helm --classic`
- Add agones repo to helm: `helm repo add agones https://agones.dev/chart/stable && helm repo update`
- Create a minikube profile for agones: `minikube start -p agones`.
- Set the minikube profile to agones: `minikube profile agones`, then install agones using helm: `helm install aimmo --namespace agones-system --create-namespace agones/agones`

#### To run Kurono:

- Ensure you are inside the python virtualenv, `pipenv shell`.
- First start the agones cluster with: `minikube start -p agones`.
- Now use `python run.py` to run the project.

## Windows setup

#### Install Manually:

- Contact a member of the Code for Life team via the [Code for Life contact form](https://www.codeforlife.education/help/#contact).

The game should now be set up to run locally. If you wish to be able to run the project with [Kubernetes](https://kubernetes.io/) and containers, follow these next steps:

- First, follow the instructions at [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to set up the frontend requirements, (you should be in the `game_frontend` folder for this step).
- Follow the instructions for [installing pyenv](https://github.com/pyenv/pyenv#installation).
- Run `pip install pipenv`, followed by `pipenv install --dev` (more information on [pipenv](https://pipenv.readthedocs.io/en/latest/)).
- Next, [download chocolatey](https://chocolatey.org/) and run `choco install kubernetes-cli`.
- Follow the instructions for [installing pyenv](https://github.com/pyenv/pyenv#installation).
- Then follow the [docker installation instructions for Windows](https://docs.docker.com/docker-for-windows/).
- Install minikube: `choco install minikube`.
- Install helm: `choco install kubernetes-helm`.
- Add agones repo to helm: `helm repo add agones https://agones.dev/chart/stable && helm repo update`.
- Create a minikube profile for agones: `minikube start -p agones`.
- Set the minikube profile to agones: `minikube profile agones`, then install agones using helm: `helm install aimmo --namespace agones-system --create-namespace agones/agones`.

#### To run Kurono:

- Ensure you are inside the python virtualenv, `pipenv shell`.
- First start the agones cluster with: `minikube start -p agones`.
- Now use `python run.py` to run the project.

## Useful information

Here you can find some other useful information regarding the setup or usage of various aspects of the project.

#### Setup script & other setup information.

- It may be the case that the frontend does not load properly upon starting aimmo (when running the script). If this is the case then you may need to follow the [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to resolve this (usually all the packages are there, it just requires you to set them up manually).
- If the script fails when attempting to install Docker, it may be because you have an old version of docker currently installed. To fix this, run: `sudo apt-get remove docker docker-engine docker.io`, then re-run the script.
- If there is an issue when using containers or the virtual enviroment. Then there small chance that VT-x/AMD-x virtualization has not been enabled on your machine. If this is the case the main way to solve this is to enable it through the BIOS settings.

#### Testing locally

- Use `./all_tests.py` to run all the tests (note that this is several pages of output).
- The `--coverage` option will generate coverage data for the tests using `coverage.py`.

#### Interacting with the cluster

- `kubectl` and `minikube` can be used to interact with the cluster.
- Running either command without any options will give the most useful commands.
- Use `minikube dashboard` to open the [Kubernetes](https://kubernetes.io/) dashboard in your browser.

#### Useful commands

- To create an another admin account: `python example_project/manage.py createsuperuser`
  - By default, we create an admin account with credentials admin:admin when you start the project.
