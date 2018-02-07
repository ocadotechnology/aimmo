# AI:MMO
A **M**assively **M**ulti-player **O**nline game, where players create **A**rtificially **I**ntelligent programs to play on their behalf.

## A [Code for Life](https://www.codeforlife.education/) project
* Ocado Technology's [Code for Life initiative](https://www.codeforlife.education/) has been developed to inspire the next generation of computer scientists and to help teachers deliver the computing curriculum.
* This repository hosts the source code of the **AI:MMO game**. AI:MMO is aimed as a follow-on from [Rapid Router](https://www.codeforlife.education/rapidrouter) to teach computing to secondary-school age children.
* The other repos for Code For Life:
    * the main portal (as well as registration, dashboards, materials...), [Code For Life Portal](https://github.com/ocadotechnology/codeforlife-portal)
    * the first coding game of Code for Life for primary schools, [Rapid Router](https://github.com/ocadotechnology/rapid-router)
    * the [deployment code for Google App Engine](https://github.com/ocadotechnology/codeforlife-deploy-appengine)

## Objective
People program Avatars. Avatars play the game. A player's aim is to create a better Avatar than other people's Avatars. A "better" Avatar is one that scores points faster than other people's Avatars.

By getting people to compete to program better Avatars, we can teach them all sorts of algorithms and optimisation techniques. For example, a really good Avatar might incorporate AI techniques such as neural networks in order to make more optimal decisions.

## The Game
The world is a 2D grid. Some cells are impassable. Some cells generate score. Some cells contain pick-ups.

There are other Avatars in the world. The more Avatars there are, the bigger the world gets.

Time passes in turns. An Avatar may perform a single action every turn. They only have visibility of a small amount of the world around them.

Avatars can only wait, move or attack.

Even with these basic mechanics, there is quite a lot of complexity in creating an Avatar that is good at gaining score. For example, you may need to be able to find optimal paths from A to B. You may need to program your Avatar to remember the parts of the world that it has already encountered, so that you can find faster paths between locations. You may need to program your Avatar to machine learn when it is optimal to:
- attack another player
- run away from another player
- try to find a health pick up
- run to the score location
- ...

## Architecture
### Web Interface - `players`
- Django
- In-browser avatar code editor: http://ace.c9.io/#nav=about
- Game view (so players can see their avatars play the game)
- Statistics
- Has a sample deployment in `example_project`

### Game creator - `aimmo-game-creator`
- Maintains the set of games

### Core Game (Simulation) - `aimmo-game`
- Maintains game state
- Simulates environment events
- Runs player actions

### Sandboxed User-Submitted AI Players (Avatars) - `aimmo-game-worker`
- Each avatar will run in their own sandbox so that we can securely deal with user-submitted code
- Each avatar will interact with the core game to get state and perform actions



## Running Locally
* Clone the repo
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

### Under Kubernetes
* By default, the local environment runs each worker in a Python thread. However, for some testing, it is useful to run as a Kubernetes cluster. Note that this is not for most testing, the default is more convenient as the Kubernetes cluster is slow and runs into resource limits with ~10 avatars.
* Linux, Windows (minikube is experimental though), and OSX (untested) are supported.
* Prerequisites:
    * All platforms: VT-x/AMD-v virtualization.
    * Linux: [Virtualbox](https://www.virtualbox.org/wiki/Downloads).
    * OSX: either [Virtualbox](https://www.virtualbox.org/wiki/Downloads) or [VMWare Fusion](http://www.vmware.com/products/fusion.html).
* Download Docker, Minikube, and Kubectl before running the script.
    * On Mac ([download homebrew](https://brew.sh/)) and run `brew update && brew install kubectl && brew cask install docker minikube virtualbox`.
* Alter your `/etc/hosts` file by adding the following to the end of the file: `192.168.99.100 local.aimmo.codeforlife.education`. You may be required to run this with `sudo` as the file is protected.
* Usage: `python run.py -k`. This will:
    * Run `minikube start` (if the cluster is not already running).
    * Images are built and a aimmo-game-creator is created in your cluster. You can preview this in your kubernetes dashboard. Run `minikube dashboard` to open this.
    * Perform the same setup that run.py normally performs.
    * Start the Django project (which is not kubernetes controlled) on localhost:8000.
* Run the same command to update all the images.

#### Interacting with the cluster
* `kubectl` and `minikube` (both in the `test-bin` folder, note that this is not on your PATH) can be used to interact with the cluster.
* Running either command without any options will give the most useful commands.
* `minikube dashboard` to open the kubernetes dashboard in your def

## Testing Locally
*`./all_tests.py` will run all tests (note that this is several pages of output).
* `--coverage` option generates coverage data using coverage.py

## Useful commands
* To create an another admin account:
`python example_project/manage.py createsuperuser`
   * By default, we create an admin account with credentials admin:admin when you start the project.

### Installing virtualenvwrapper on Mac
* Run `pip install virtualenvwrapper`
* Add the following to ~/.bashrc:
```
 export WORKON_HOME=$HOME/.virtualenvs
 source /usr/local/bin/virtualenvwrapper.sh
```
* [This blog post](http://mkelsey.com/2013/04/30/how-i-setup-virtualenv-and-virtualenvwrapper-on-my-mac/) may also be
 useful.

## Common/Known Issues
* If you get an error saying `no module named google.auth` after trying to run `./run.py` or `./run.py -k`, rerun the command again and the dependency should be detected. This is a [logged issue][auth-issue] and we are working to solve it.
[auth-issue]: https://github.com/ocadotechnology/aimmo/issues/449
* When deploying with semaphoreCI, the cache may be old and corrupt one of the packages being installed by `pip`. The error you may get may look like this `error: Error -5 while decompressing data: incomplete or truncated stream`. You need to `ssh` into the appropriate server and delete the cache directory. Another solution is to `pip install` with the `--no-cache-dir` flag but we do not recommend this.

## How to contribute!
__Want to help?__ You can read the [contributing guidelines][contrib-guidelines]. You can also contact us directly using this [contact form][c4l-contact-form] and we'll get in touch as soon as possible! Thanks a lot.

[c4l-contact-form]: https://www.codeforlife.education/help/#contact
[contrib-guidelines]: https://github.com/ocadotechnology/aimmo/blob/master/CONTRIBUTING.md

