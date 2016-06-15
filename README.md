# AI:MMO
A **M**assively **M**ulti-player **O**nline game, where players create **A**rtificially **I**ntelligent programs to play on their behalf.

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
* Make and activate a virtualenv (We recommend [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/index.html)) - if you have a Mac see the following section.
    * e.g. the first time, `mkvirtualenv -a path/to/aimmo aimmo`
    * and thereafter `workon aimmo`
* You might need to create an admin account the first time around:
`python example_project/manage.py createsuperuser`
* `./run` in your aimmo dir - This will:
    * install all of the dependencies using pip
    * sync the database
    * collect the static files
    * run the server

### Installing virtualenvwrapper on Mac
* Run `pip install virtualenvwrapper`
* Add the following to ~/.bashrc:
```
 export WORKON_HOME=$HOME/.virtualenvs
 source /usr/local/bin/virtualenvwrapper.sh
```
* [This blog post](http://mkelsey.com/2013/04/30/how-i-setup-virtualenv-and-virtualenvwrapper-on-my-mac/) may also be
 useful.
