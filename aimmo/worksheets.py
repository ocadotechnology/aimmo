from dataclasses import dataclass
from typing import List


@dataclass
class Worksheet:
    id: int
    name: str
    era: int
    starter_code: str
    active_image_path: str
    description: str
    image_path: str
    short_description: str
    thumbnail_text: str
    student_challenge_url: str

    def __post_init__(self):
        # Remove spaces around starter_code and add a new line
        self.starter_code = self.starter_code.strip() + "\n"


WORKSHEETS = {
    1: Worksheet(
        id=1,
        name="Present Day I: The Museum",
        era=1,
        starter_code="""
#-------------------------------------------------------------------------------
#  Worksheet 1 challenges:
#    Task 1: Change direction
#       - The starter code moves your avatar North. Change this code so that it
#         moves in a different direction.
#
#    Task 2: Move in all directions
#       - Write some code that moves your avatar in a random direction. Don't
#         forget to add `import random` at the top of your code.
#
#    Task 3: Investigate location
#       - Investigate what `print(avatar_state.location)` tells you and then
#         check if you can move to the next location
#
#  New commands:
#       - MoveAction(DIRECTION)
#       - avatar_state.location -> LOCATION
#       - world_state.can_move_to(LOCATION) -> True/False
#
#-------------------------------------------------------------------------------
def next_turn(world_state, avatar_state):
    new_dir = direction.NORTH
    #  Your code goes here
    action = MoveAction(new_dir)
    return action
""",
        active_image_path="images/worksheets/future_active.png",
        description="While working at the Scriptsonian museum for class credit, you have accidentally activated the mysterious Kurono time machine! The museum’s valuable artefacts are scattered across the shelves, the floor, the whole spacetime continuum. It’s going to take more than just a backpack to collect them all. You need to use the Kurono time machine to get them back – but before jumping in you need to learn how to use its navigation system. This challenge shows you how to move around the map so you don’t run into problems in the future…or past.",
        image_path="images/worksheets/future.jpg",
        short_description="While working at the Scriptsonian museum for class credit, you have accidentally activated the mysterious Kurono time machine!",
        thumbnail_text="",
        student_challenge_url="https://code-for-life.gitbook.io/learning-resources/student-challenges/student-challenge-1",
    ),
    2: Worksheet(
        id=2,
        name="Present Day II",
        era=1,
        starter_code="""
#-------------------------------------------------------------------------------
#  Worksheet 2 challenges:
#    Task 1: Avoiding obstacles
#       - Change the code so that your avatar tries a different direction if
#         they are unable to move. To avoid repeating code, create a subroutine
#         called get_random_dir() and use it to return a random direction.
#
#    Task 2: Pick up an artefact
#       - Pick up any artefacts you find on the board. If the location you are
#         in contains an artefact, you can pick it up by returning a
#         PickupAction() instead of a MoveAction(DIRECTION).
#
#  New commands:
#       - action = PickupAction()
#
#  Previous commands:
#       - avatar_state.location -> LOCATION
#       - MoveAction(DIRECTION)
#       - world_state.can_move_to(LOCATION) -> True/False
#-------------------------------------------------------------------------------
import random

def next_turn(world_state, avatar_state):
    #  Choose a random direction to move in
    number = random.randint(1,4)
    if number == 1:
        new_dir = direction.NORTH
    elif number == 2:
        new_dir = direction.EAST
    elif number == 3:
        new_dir = direction.SOUTH
    else:
        new_dir = direction.WEST
    #  Get details about the location you would move onto
    next_location = avatar_state.location + new_dir
    if world_state.can_move_to(next_location):
        #  This location is free
        action = MoveAction(new_dir)
    else:
        print("I can't move that way!")
        action = WaitAction()
    return action
""",
        active_image_path="images/worksheets/future2_active.png",
        description="Now that you know how to navigate, it’s time to clean up the evidence before leaving this timeline!  Some of the artefacts escaped the vortex and ended up all over the museum - if each of you picks one of them up, you should be ready to embark on your journey!",
        image_path="images/worksheets/future.jpg",
        short_description="Now that you know how to navigate, it’s time to clean up the evidence before leaving this timeline!",
        thumbnail_text="",
        student_challenge_url="https://code-for-life.gitbook.io/learning-resources/student-challenges/student-challenge-2",
    ),
    3: Worksheet(
        id=3,
        name="Ancient",
        era=2,
        starter_code="""
#-------------------------------------------------------------------------------
#  Worksheet 3 challenges:
#     Task 1: Direction control
#       - Return MoveTowardsAction(ARTEFACT) to move towards the nearest
#         artefact.
#       - You can use world_state.scan_nearby() to get a list of nearby
#         artefacts.
#       - You must check that the list is not empty before reading a value from
#         it.
#
#     Task 2: Pick up five artefacts
#       - Pick up five artefacts on the board. Check your backpack to see how
#         many you are holding using `avatar_state.backpack`. Output a message
#         when you have picked up five.
#
#     Task 3: Types of artefacts
#       - Part 1: Use `artefact.type` where `artefact` is an item of
#         `avatar_state.backpack` to list all types of artefacts in your
#         backpack.
#       - Part 2: Output a summary of your backpack using the same
#         `artefact.type` as above. e.g. I have 3 keys and 2 chests.
#
#  New commands:
#       - world_state.scan_nearby() -> LIST OF ARTEFACTS
#       - MoveTowardsAction(ARTEFACT)
#       - avatar_state.backpack -> LIST OF HELD ARTEFACTS
#       - artefact.type -> TYPE (e.g. artefact_types.KEY or artefact_types.CHEST)
#
#  Previous commands:
#       - avatar_state.location -> LOCATION
#       - MoveAction(DIRECTION)
#       - world_state.can_move_to(LOCATION) -> True/False
#       - action = PickupAction()
#-------------------------------------------------------------------------------
def next_turn(world_state, avatar_state):
    new_dir = direction.NORTH
    #  Your code goes here
    action = MoveAction(new_dir)
    return action
""",
        active_image_path="images/worksheets/ancient_active.png",
        description="You are now familiar with your equipment and have managed to unlock the gateway to the first time checkpoint. You find yourself in a strange place, full of familiar structures in the form of ruins. You see artefacts of different types scattered around you, where to start? Luckily, your navigator is working... You can use it to scan your surroundings and walk towards the artefacts. If you and your friends pick up five artefacts each, you should be done in no time!",
        image_path="images/worksheets/ancient.jpg",
        short_description="You find yourself in a strange place, full of familiar structures in the form of ruins.",
        thumbnail_text="",
        student_challenge_url="https://code-for-life.gitbook.io/learning-resources/student-challenges/student-challenge-3",
    ),
    4: Worksheet(
        id=4,
        name="21st Century",
        era=3,
        starter_code="""
#-------------------------------------------------------------------------------
#  Worksheet 4 challenges:
#    Task 1: Examine your backpack
#       - Change the code so that you can print how many items are in your backpack.
#       - Print the first item from your backpack and the item type.
#
#    Task 2: Examine all artefacts
#       - Write some code that outputs the position and description of each
#         of the artefact in your backpack.
#
#    Task 3: Count your loot
#       - Count how many you have of each artefact.
#
#    Task 4: Drop artefacts by type
#       - Drop artefacts that you do not need.
#
#  New commands:
#       - DropAction(index)
#       - backpack.find(ARTEFACT_TYPE)
#
#  Previous commands:
#       - world_state.scan_nearby() -> LIST OF ARTEFACTS
#       - MoveTowardsAction(ARTEFACT)
#       - avatar_state.backpack -> LIST OF HELD ARTEFACTS
#       - artefact.type -> TYPE
#-------------------------------------------------------------------------------

def next_turn(world_state, avatar_state):
    # Find out where your avatar is
    avatar_location = avatar_state.location
    current_cell = world_state.get_cell(avatar_location)

    # Check if the current cell holds an artefact
    if current_cell.has_artefact():
        # It does! Pick it up.
        action = PickupAction()
    else:
        # The cell does not contain an artefact
        # Find the location of all artefacts nearby
        nearby = world_state.scan_nearby(avatar_location)

        # Get the nearest one
        nearest = nearby[0]

        # Move towards the nearest arteface
        action = MoveTowardsAction(nearest)

    return action
""",
        active_image_path="images/worksheets/modern_active.png",
        description="After successfully collecting all the missing artefacts from the first time checkpoint, you arrive at what looks like the 21st century. You recognise some cars parked here and there, just like the ones your history teacher told you about. In this timeline, there seems to be some object which will have no value in the museum.",
        image_path="images/worksheets/modern.jpg",
        short_description="After successfully collecting all the missing artefacts from the first time checkpoint, you arrive at what looks like the 21st century.",
        thumbnail_text="",
        student_challenge_url="https://code-for-life.gitbook.io/learning-resources/student-challenges/student-challenge-4",
    ),
    5: Worksheet(
        id=5,
        name="Prehistoric",
        era=4,
        starter_code="""
def next_turn(world_state, avatar_state):
    new_dir = direction.NORTH
    # Your code goes here
    action = MoveAction(new_dir)
    return action
""",
        active_image_path="images/worksheets/prehistory_active.png",
        description="Oh no! Looks like the time machine has taken you even further back in time. You find yourself in a place that looks very… wild. You can hear the occasional distant roaring, added to the buzzing of what sound like  gigantic  insects. Vegetation is so abundant around you that you can barely move. It might be a good idea to use your navigation system to scan all around you before even trying! And don’t forget to keep track of the portal that’ll send you back to your original timeline - just in case something with sharp teeth starts running towards you.",
        image_path="images/worksheets/prehistory.jpg",
        short_description="Oh no! Looks like the time machine has taken you even further back in time. You find yourself in a place that looks very… wild.",
        thumbnail_text="Coming Soon",
        student_challenge_url="",
    ),
    6: Worksheet(
        id=6,
        name="Back to the Future",
        era=5,
        starter_code="""
def next_turn(world_state, avatar_state):
    new_dir = direction.NORTH
    # Your code goes here
    action = MoveAction(new_dir)
    return action
""",
        active_image_path="images/worksheets/broken_future_active.png",
        description="You’ve made it! Well, almost. You’re back to your original time, but something seems to be off. The museum is still there, with all the chaos you still need to tidy up, but the environment isn’t quite right. The electronic containers and shelves seem slightly different, and when the AI interlocutor speaks, you don’t recognise the language. It looks like you’ve changed something in the past that affected events in your present! If you manage to extract the metadata from the recovered artefacts, you should be able to find out which timelines they were found in. You can input this text into the Kurono machine to get things back to normal.",
        image_path="images/worksheets/broken_future.jpg",
        short_description="You’ve made it! Well, almost. You’re back to your original time, but something seems to be off.",
        thumbnail_text="Coming Soon",
        student_challenge_url="",
    ),
}


def get_complete_worksheets() -> List[Worksheet]:
    return [worksheet for worksheet in WORKSHEETS.values() if worksheet.thumbnail_text != "Coming Soon"]


def get_incomplete_worksheets() -> List[Worksheet]:
    return [worksheet for worksheet in WORKSHEETS.values() if worksheet.thumbnail_text == "Coming Soon"]


def get_worksheets_excluding_id(id: int) -> List[Worksheet]:
    return [worksheet for worksheet in WORKSHEETS.values() if worksheet.id != id]
