from __future__ import absolute_import

import asyncio
import json

from tests.test_simulation.concrete_worker import ConcreteWorker

from httmock import HTTMock
from simulation.avatar import avatar_wrapper
from simulation.location import Location


class MockEffect(object):
    def __init__(self, avatar):
        self.turns = 0
        self.is_expired = False
        self.removed = False
        self.expire = False
        self.avatar = avatar

    def on_turn(self):
        self.is_expired = self.expire
        self.turns += 1

    def remove(self):
        self.removed = True
        self.avatar.effects.remove(self)


class MockAction(object):
    def __init__(self, avatar, **options):
        global actions_created
        self.options = options
        self.avatar = avatar
        actions_created.append(self)


class ActionRequest(object):
    def __init__(self, options=None):
        if options is None:
            options = {}
        self.options = options

    def __call__(self, url, request):
        return json.dumps({"action": {"action_type": "test", "options": self.options}})


def InvalidJSONRequest(url, request):
    return "EXCEPTION"


def NonExistentActionRequest(url, request):
    return json.dumps({"action": {"action_type": "fake", "option": {}}})


avatar_wrapper.ACTIONS = {"test": MockAction}


class TestAvatarWrapper:
    def setup_method(self):
        global actions_created
        actions_created = []
        self.worker = ConcreteWorker(1, 0)
        self.avatar = avatar_wrapper.AvatarWrapper(
            player_id=None, initial_location=None, avatar_appearance=None
        )

    async def take_turn(self, request_mock):
        with HTTMock(request_mock):

            worker_data = await self.worker.fetch_data(None)
            self.avatar.decide_action(worker_data)

    async def test_bad_action_data_given(self, loop):
        request_mock = InvalidJSONRequest
        await self.take_turn(request_mock)
        assert actions_created == [], "No action should have been applied"

    async def test_non_existant_action(self, loop):
        request_mock = NonExistentActionRequest
        await self.take_turn(request_mock)
        assert actions_created == [], "No action should have been applied"

    def add_effects(self, num=2):
        effects = []
        for _ in range(num):
            effect = MockEffect(self.avatar)
            self.avatar.effects.add(effect)
            effects.append(effect)
        return effects

    def test_effects_on_turn_are_called(self):
        effect1, effect2 = self.add_effects()
        self.avatar.update_effects()
        assert effect1.turns == 1
        assert effect2.turns == 1

    def test_effects_not_removed(self):
        effect1, effect2 = self.add_effects()
        self.avatar.update_effects()
        assert set((effect1, effect2)) == self.avatar.effects

    def test_expired_effects_removed(self):
        effect1, effect2 = self.add_effects()
        effect1.expire = True
        self.avatar.update_effects()
        assert effect2.turns == 1
        assert self.avatar.effects == set((effect2,))

    def test_effects_applied_on_invalid_action(self):
        self.take_turn(InvalidJSONRequest)
        effect = self.add_effects(1)[0]
        self.avatar.update_effects()
        assert effect.turns == 1

    def test_avatar_dies_health(self):
        self.avatar.die(None)
        assert self.avatar.health == 5

    def test_avatar_dies_score_when_large(self):
        self.avatar.score = 10
        self.avatar.die(None)
        assert self.avatar.score == 8

    def test_avatar_dies_score_when_small(self):
        self.avatar.score = 1
        self.avatar.die(None)
        assert self.avatar.score == 0

    def test_avatar_dies_location(self):
        self.avatar.die("test")
        assert self.avatar.location == "test"

    def test_damage_applied(self):
        self.avatar.health = 10
        assert self.avatar.damage(1) == 1
        assert self.avatar.health == 9

    def test_resistance_reduces_damage(self):
        self.avatar.health = 10
        self.avatar.resistance = 3
        assert self.avatar.damage(5) == 2
        assert self.avatar.health == 8

    def test_no_negative_damage(self):
        self.avatar.health = 10
        self.avatar.resistance = 3
        assert self.avatar.damage(1) == 0
        assert self.avatar.health == 10

    def test_calculate_orientation(self):
        # East movement
        self.avatar.location = Location(0, 0)
        self.avatar.previous_location = Location(-1, 0)

        assert self.avatar.calculate_orientation() == "east"
