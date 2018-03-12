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


## Quick Start
1. Clone the repo. Preferably the master branch.
2. Take a look at our [usage guidelines](docs/usage.md) to see how to get started.

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

## Documentation
Take a look at our [documentation table of contents][docs/FAQ.md]. This is available offline along with
the project.

## How to contribute!
__Want to help?__ You can read the [contributing guidelines][contrib-guidelines]. You can also contact us directly using this [contact form][c4l-contact-form] and we'll get in touch as soon as possible! Thanks a lot.

[c4l-contact-form]: https://www.codeforlife.education/help/#contact
[contrib-guidelines]: https://github.com/ocadotechnology/aimmo/blob/master/CONTRIBUTING.md
