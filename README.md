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
* Make and activate a **Python 2.7** virtualenv (We recommend [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/index.html)) - if you have a Mac see the following section. 
    * e.g. the first time, `mkvirtualenv -a path/to/aimmo aimmo`
    * and thereafter `workon aimmo`
    * If you have multiple Python versions installed, you can specify an interpreter for the virtualenv with the `--python=/path/to/python` flag
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
* Usage: `python run.py -k`. This will:
    * Download Docker, Minikube, and Kubectl into a `test-bin` folder in the project's root directory.
    * Run `minikube start` (if the cluster is not already running).
    * Build each image.
    * Start aimmo-game-creator.
    * Perform the same setup that run.py normally performs.
    * Start the Django project (which is not kubernetes controlled) on localhost:8000.
* Run the same command to update all the images.

#### Interacting with the cluster
* `kubectl` and `minikube` (both in the `test-bin` folder, note that this is not on your PATH) can be used to interact with the cluster.
* Running either command without any options will give the most useful commands.
* `./test-bin/minikube dashboard` to open the kubernetes dashboard in your def

## Testing Locally
*`./all_tests.py` will run all tests (note that this is several pages of output).
* `--coverage` option generates coverage data using coverage.py

## Useful commands
* To create an admin account:
`python example_project/manage.py createsuperuser`

### Installing virtualenvwrapper on Mac
* Run `pip install virtualenvwrapper`
* Add the following to ~/.bashrc:
```
 export WORKON_HOME=$HOME/.virtualenvs
 source /usr/local/bin/virtualenvwrapper.sh
```
* [This blog post](http://mkelsey.com/2013/04/30/how-i-setup-virtualenv-and-virtualenvwrapper-on-my-mac/) may also be
 useful.

## How to contribute!
__Want to help?__ You can contact us using this [contact form][c4l-contact-form] and we'll get in touch as soon as possible! Thanks a lot.

[c4l-contact-form]: https://www.codeforlife.education/help/#contact
