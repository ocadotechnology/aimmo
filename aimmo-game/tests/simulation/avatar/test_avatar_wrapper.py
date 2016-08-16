from __future__ import absolute_import
import json
from httmock import HTTMock
from simulation.avatar import avatar_wrapper
from unittest import TestCase


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
    def __init__(self, **options):
        global actions_created
        self.options = options
        self.applied_to = None
        actions_created.append(self)

    def apply(self, game_state, avatar):
        self.applied_to = avatar


class ActionRequest(object):
    def __init__(self, options=None):
        if options is None:
            options = {}
        self.options = options

    def __call__(self, url, request):
        return json.dumps({'action': {'action_type': 'test', 'options': self.options}})


def InvalidJSONRequest(url, request):
    return 'EXCEPTION'


def NonExistantActionRequest(url, request):
    return json.dumps({'action': {'action_type': 'fake', 'option': {}}})


avatar_wrapper.ACTIONS = {
    'test': MockAction
}


class TestAvatarWrapper(TestCase):
    def setUp(self):
        global actions_created
        actions_created = []
        self.avatar = avatar_wrapper.AvatarWrapper(None, None, 'http://test', None)

    def take_turn(self, request_mock=None):
        if request_mock is None:
            request_mock = ActionRequest()
        with HTTMock(request_mock):
            self.avatar.take_turn(None, None)

    def test_action_applied(self):
        self.take_turn()
        self.assertGreater(len(actions_created), 0, 'No action applied')
        self.assertEqual(len(actions_created), 1, 'Too many actions applied')
        self.assertEqual(actions_created[0].applied_to, self.avatar, 'Action applied on wrong avatar')

    def test_bad_action_data_given(self):
        request_mock = InvalidJSONRequest
        self.take_turn(request_mock)
        self.assertEqual(actions_created, [], 'No action should have been applied')

    def test_non_existant_action(self):
        request_mock = NonExistantActionRequest
        self.take_turn(request_mock)
        self.assertEqual(actions_created, [], 'No action should have been applied')

    def add_effects(self, num=2):
        effects = []
        for _ in xrange(num):
            effect = MockEffect(self.avatar)
            self.avatar.effects.add(effect)
            effects.append(effect)
        return effects

    def test_effects_on_turn_are_called(self):
        effect1, effect2 = self.add_effects()
        self.take_turn()
        self.assertEqual(effect1.turns, 1)
        self.assertEqual(effect2.turns, 1)

    def test_effects_not_removed(self):
        effect1, effect2 = self.add_effects()
        self.take_turn()
        self.assertEqual(set((effect1, effect2)), self.avatar.effects)

    def test_expired_effects_removed(self):
        effect1, effect2 = self.add_effects()
        effect1.expire = True
        self.take_turn()
        self.assertEqual(effect2.turns, 1)
        self.assertEqual(self.avatar.effects, set((effect2,)))

    def test_effects_applied_on_invalid_action(self):
        self.take_turn(InvalidJSONRequest)
        effect = self.add_effects(1)[0]
        self.take_turn()
        self.assertEqual(effect.turns, 1)
