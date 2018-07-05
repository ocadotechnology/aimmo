# Usage
- [Running Locally with no containers](#running-locally-with-no-containers)
- [Running with Kubernetes with containers](#running-with-kubernetes-with-containers)
- [Testing Locally](#testing-locally)
- [Useful Commands](#useful-commands)
- [Installing pipenv](#installing-pipenv)
---

## Running Locally with no containers
* Follow the instructions at [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to install all the frontend requirements.
* Make and activate a virtualenv (We recommend [pipenv](https://docs.pipenv.org/)) - if you have a **[Mac see the section at the bottom](https://github.com/ocadotechnology/aimmo/blob/master/docs/usage.md#on-mac)**.
    * To set this up, run `./ubuntu_setup.sh`. This will install nodejs, yarn, as well as pipenv. 
    * The next time you would like to use your virtualenv, run `pipenv shell`.
* `./run.py` in your aimmo dir - This will:
    * if necessary, create a superuser 'admin' with password 'admin'
    * install all of the dependencies using pip
    * sync the database
    * collect the static files
    * run the server
* You can quickly create players as desired using the following command:

  `python example_project/manage.py generate_players 5 dumb_avatar.py`

  This creates 5 users with password `123`, and creates for each user an avatar that runs the code in `dumb_avatar.py`
* To delete the generated players use the following command:

`python example_project/manage.py delete_generated_players`


## Running with Kubernetes with containers
**64bit environment is required for this mode!**
* Follow the instructions at [game frontend documentation](https://github.com/ocadotechnology/aimmo/blob/master/game_frontend/README.md) in order to install all the frontend requirements.
* By default, the local environment runs each worker in a Python thread. This is the closest mode that reflects the environment in production. However, this will require much more resources.
* Linux, Windows, and OSX.
* Prerequisites:
    * All platforms: VT-x/AMD-v virtualization.
    * Linux: [Virtualbox](https://www.virtualbox.org/wiki/Downloads).
    * OSX: either [Virtualbox](https://www.virtualbox.org/wiki/Downloads) or [VMWare Fusion](http://www.vmware.com/products/fusion.html).
* To download Docker, Minikube, and Kubectl before running the script. 
    * On Mac ([download homebrew](https://brew.sh/)) and run `brew update && brew cask install docker virtualbox`. 
        * Install a fixed minikube version (at the time of this article this is 0.25.2 but you can confirm that [here](https://github.com/ocadotechnology/aimmo/blob/b0fd1bf852b1b2630a8546d173798ec9a670c480/.travis.yml#L23)). To do this write 
        `curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
        ` and replace the version with the desired one. 
        * Install kubectl: 
        `curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.9.4/bin/darwin/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
    * On Ubuntu ([download snap](https://snapcraft.io/)) and run `sudo snap install kubectl --classic` then follow the ([docker installation instructions](https://docs.docker.com/install/linux/docker-ce/ubuntu/)).
    * On Windows ([download chocolatey](https://chocolatey.org/)) and run `choco install kubernetes-cli` followed by the ([docker installation instructions for Windows](https://docs.docker.com/docker-for-windows/)).
* Alter your `/etc/hosts` file by adding the following to the end of the file: `192.168.99.100 local.aimmo.codeforlife.education`. You may be required to run this with `sudo` as the file is protected.
* Usage: `python run.py -k`. This will:
    * Run `minikube start --memory=2048 -cpus=2`. Feel free to change these values appropriately to your specifiation.
    * Images are built and a aimmo-game-creator is created in your cluster. You can preview this in your kubernetes dashboard. Run `minikube dashboard` to open this.
    * Perform the same setup that run.py normally performs.
    * Start the Django project (which is not kubernetes controlled) on localhost:8000.
* Run the same command to update all the images.

### Interacting with the cluster

* `kubectl` and `minikube` can be used to interact with the cluster.
* Running either command without any options will give the most useful commands.
* `minikube dashboard` to open the kubernetes dashboard in your browser.

## Testing Locally
*`./all_tests.py` will run all tests (note that this is several pages of output).
* `--coverage` option generates coverage data using coverage.py

## Useful Commands
* To create an another admin account:
`python example_project/manage.py createsuperuser`
   * By default, we create an admin account with credentials admin:admin when you start the project.
   
## Installing pipenv
### On Mac:
* Run `brew install pipenv`
* To activate your virtualenv, run `pipenv shell`

