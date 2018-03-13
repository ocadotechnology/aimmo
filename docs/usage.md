# Usage
- [Running Locally with no containers](#running-locally-with-no-containers)
- [Running with Kubernetes with containers](#running-with-kubernetes-with-containers)
- [Testing Locally](#testing-locally)
- [Useful Commands](#useful-commands)
- [Installing virtualenvwrapper](#installing-virtualenvwrapper)
---

## Running Locally with no containers
* Make and activate a virtualenv (We recommend [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/index.html)) - if you have a **[Mac see the section at the bottom](https://github.com/ocadotechnology/aimmo#installing-virtualenvwrapper-on-mac)**.
    * e.g. the first time, `mkvirtualenv -a path/to/aimmo aimmo`
    * and thereafter `workon aimmo`
    * You may need to set your virtualenvwrapper version to python2. [See more here](https://stackoverflow.com/questions/32489304/change-default-python-version-with-virtualenvwrapper-virtualenv).
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
* By default, the local environment runs each worker in a Python thread. However, for some testing, it is useful to run as a Kubernetes cluster. Note that this is not for most testing, the default is more convenient as the Kubernetes cluster is slow and runs into resource limits with ~10 avatars.
* Linux, Windows (minikube is experimental though), and OSX (untested) are supported.
* Prerequisites:
    * All platforms: VT-x/AMD-v virtualization.
    * Linux: [Virtualbox](https://www.virtualbox.org/wiki/Downloads).
    * OSX: either [Virtualbox](https://www.virtualbox.org/wiki/Downloads) or [VMWare Fusion](http://www.vmware.com/products/fusion.html).
* Download Docker, Minikube, and Kubectl before running the script.
    * On Mac ([download homebrew](https://brew.sh/)) and run `brew update && brew install kubectl && brew cask install docker minikube virtualbox`.
    * On Ubuntu ([download snap](https://snapcraft.io/)) and run `sudo snap install kubectl --classic` then follow the ([docker installation instructions](https://docs.docker.com/install/linux/docker-ce/ubuntu/)).
    * On Windows ([download chocolatey](https://chocolatey.org/)) and run `choco install kubernetes-cli` followed by the ([docker installation instructions for Windows](https://docs.docker.com/docker-for-windows/)).
* Alter your `/etc/hosts` file by adding the following to the end of the file: `192.168.99.100 local.aimmo.codeforlife.education`. You may be required to run this with `sudo` as the file is protected.
* Usage: `python run.py -k`. This will:
    * Run `minikube start` (if the cluster is not already running).
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
   
## Installing virtualenvwrapper
### On Mac:
* Run `pip install virtualenvwrapper`
* Add the following to ~/.bashrc:
```
 export WORKON_HOME=$HOME/.virtualenvs
 source /usr/local/bin/virtualenvwrapper.sh
```
* [This blog post](http://mkelsey.com/2013/04/30/how-i-setup-virtualenv-and-virtualenvwrapper-on-my-mac/) may also be
 useful.
