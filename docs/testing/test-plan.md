# Manual Test Plan
- [Level 1](#level-1)
- [Custom Games](#custom-games)
- [Out Of Testing Scope](#out-of-testing-scope)
---

**Prerequisites**
* Delete the database file in example_project/example_project/db.sqlite3.
* First run the test using `./run.py` and then try `./run.py -k`.
* Make sure to open your terminal to see for any messages. Some exceptions are expected but keep note.
***


## Level 1
### Check the following:

**Prior to playing the game:**
* The level exists already. Check it by navigating to the Watch->Level.
* If required, you can login using your details (admin:admin default).
* You are at the correct URL (/kurono/watch_level/1/).
* It consists of **_five_** square boxes lined horizontally. The leftmost is at (-2,0), the right most at (2,0).
* There is no player on the screen. Nothing is happening.

**Programming the game:**
* Program the game (Program-> Level1) and end up in the correct URL (kurono/program_level/1/).
* Ensure the code will be able to move the character to the right 4 times. Default code will suffice (see below to copy). 
* Click the save button. Now go to Watch->Level1 via the menu (or press the Watch hotlink above the editor).
* See the character moving. It should stop when it gets to red box at (2,0). 

```
class Avatar(object):
    def next_turn(self, world_view, events):
        from simulation.action import MoveAction
        from simulation.direction import ALL_DIRECTIONS
        import random

        return MoveAction(random.choice(ALL_DIRECTIONS))
```

***

## Custom Games
### Check the following:
**Prior to playing the game:**
* Ensure there are no custom games running (Watch menu).
* Go to Program->Create a new game (/kurono/games/new). Select any name, select yourself in the 'Can Play' menu.
* Ensure 'Generator' is set to "Open World". Save, watch.
* A grid should show with an avatar moving around randomly.
* The score location should move randomly from time to time (depending on settings).
* Score of the avatar should increase as the avatar passes onto it.
* Pickups (3 types) should spawn from time to time.
   1. Any of the types should disappear after an avatar passes through the same cell.
   2. Health pickup (white with red cross) should restore the avatar's health (the hp text).
   3. The other two pickups (blue: invulnerability, red: damage boost) should appear, but have no visible effect on the avatar yet.
* Health of an avatar should be able to decrease. On 0, the avatar should respawn.
* Follow the instructions on the main homepage to see how you can add multiple avatars to a game at the same time.
***

## Out of testing scope
### Check the following:
* Reprogram the game to your own behavior. Check everything is done as expected.
***
