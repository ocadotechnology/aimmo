import logging

from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from players import models, views

views.app_settings.GAME_SERVER_URL_FUNCTION = lambda game_id: ('base %s' % game_id, 'path %s' % game_id)
views.app_settings.GAME_SERVER_PORT_FUNCTION = lambda game_id: 0
views.app_settings.GAME_SERVER_SSL_FLAG = True


class TestViews(TestCase):
    CODE = 'class Avatar: pass'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('test', 'test@example.com', 'password')
        cls.user.is_staff = True
        cls.user.save()
        cls.game = models.Game(id=1, name='test')
        cls.game.save()

    def setUp(self):
        self.game.refresh_from_db()

    def login(self):
        c = Client()
        c.login(username='test', password='password')
        return c

    def test_add_new_code(self):
        c = self.login()
        response = c.post(reverse('aimmo/code', kwargs={'id': 1}), {'code': self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Avatar.objects.get(owner__username='test').code, self.CODE)

    def test_update_code(self):
        c = self.login()
        models.Avatar(owner=self.user, code='test', game=self.game).save()
        response = c.post(reverse('aimmo/code', kwargs={'id': 1}), {'code': self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Avatar.objects.get(owner__username='test').code, self.CODE)

    def test_code_for_non_existant_game(self):
        c = self.login()
        response = c.post(reverse('aimmo/code', kwargs={'id': 2}), {'code': self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_code_for_non_authed_user(self):
        self.game.public = False
        self.game.save()
        c = self.login()
        response = c.post(reverse('aimmo/code', kwargs={'id': 1}), {'code': self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_login_required_for_code(self):
        self.game.public = False
        self.game.can_play = [self.user]
        self.game.save()
        c = Client()
        response = c.post(reverse('aimmo/program', kwargs={'id': 1}), {'code': self.CODE})
        self.assertNotEqual(response.status_code, 200)

    def test_default_code(self):
        c = self.login()
        response = c.get(reverse('aimmo/code', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith('class Avatar'))

    def test_retrieve_code(self):
        models.Avatar(owner=self.user, code=self.CODE, game=self.game).save()
        c = self.login()
        response = c.get(reverse('aimmo/code', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.CODE)

    def test_program(self):
        c = self.login()
        response = c.get(reverse('aimmo/program', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['game_id'], 1)

    def test_program_for_non_existant_game(self):
        c = self.login()
        response = c.get(reverse('aimmo/program', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 404)

    def test_program_for_non_authed_user(self):
        self.game.public = False
        self.game.save()
        c = self.login()
        response = c.get(reverse('aimmo/program', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    def _associate_game_as_level_num(self, level_num=1, user=None, game=None):
        if game is None:
            game = self.game
        if user is None:
            user = self.user
        models.LevelAttempt(user=user, game=game, level_number=level_num).save()
        models.Game(name='Wrong').save()

    def test_program_level(self):
        self._associate_game_as_level_num()
        c = self.login()
        response = c.get(reverse('aimmo/program_level', kwargs={'num': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['game_id'], 1)

    def test_program_level_creates_level(self):
        if models.Game.objects.filter(levelattempt__user=self.user, levelattempt__level_number=1).exists():
            self.skipTest('DB is polluted, alreaday a level attempt for level 1')
        c = self.login()
        response = c.get(reverse('aimmo/program_level', kwargs={'num': 1}))
        self.assertEqual(response.status_code, 200)
        game = models.Game.objects.get(id=response.context['game_id'])
        self.assertEqual(game.name, 'Level 1', 'Game name should be "Level 1"')
        self.assertEqual(game.owner, None, 'Game should not have an owner')
        self.assertEqual(game.public, False, 'Game should not be public')
        self.assertEqual(list(game.can_play.all()), [self.user], 'Game should be playable by current user')
        self.assertEqual(game.completed, False, 'Game should not be completed')
        self.assertEqual(game.main_user, self.user, 'Game should have current user as main user')
        self.assertEqual(game.generator, 'Level1', 'Game should use "Level1" generator')
        self.assertEqual(game.levelattempt.user, self.user, 'Game should be an attempt for the current user')
        self.assertEqual(game.levelattempt.level_number, 1, 'Game should be an attempt at level 1')

    def test_program_level_too_high(self):
        c = self.login()
        # We cause a warning by using a level too high which is expected
        logging.disable(logging.WARNING)
        response = c.get(reverse('aimmo/program_level', kwargs={'num': 1000}))
        logging.disable(logging.INFO)
        self.assertEqual(response.status_code, 404)

    def test_watch(self):
        c = self.login()
        response = c.get(reverse('aimmo/watch', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_user_player_key'], self.user.pk)
        self.assertEqual(response.context['game_url_base'], 'base 1')
        self.assertEqual(response.context['game_url_path'], 'path 1')

    def test_watch_for_non_existant_watch(self):
        c = self.login()
        response = c.get(reverse('aimmo/watch', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 404)

    def test_watch_for_non_authed_user(self):
        self.game.public = False
        self.game.save()
        c = self.login()
        response = c.get(reverse('aimmo/watch', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_watch_level(self):
        self._associate_game_as_level_num()
        c = self.login()
        response = c.get(reverse('aimmo/watch_level', kwargs={'num': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_user_player_key'], self.user.pk)
        self.assertEqual(response.context['game_url_base'], 'base 1')
        self.assertEqual(response.context['game_url_path'], 'path 1')

    def test_watch_level_creates_level(self):
        if models.Game.objects.filter(levelattempt__user=self.user, levelattempt__level_number=1).exists():
            self.skipTest('DB polluted, already a level attempt present')
        c = self.login()
        response = c.get(reverse('aimmo/watch_level', kwargs={'num': 1}))
        self.assertEqual(response.status_code, 200)
        game = models.Game.objects.get(levelattempt__user=self.user, levelattempt__level_number=1)
        self.assertEqual(list(game.can_play.all()), [self.user], 'Game should be playable by current user')
        self.assertEqual(game.completed, False, 'Game should not be completed')
        self.assertEqual(game.main_user, self.user, 'Game should have current user as main user')
        self.assertEqual(game.generator, 'Level1', 'Game should use "Level1" generator')
        self.assertEqual(game.levelattempt.user, self.user, 'Game should be an attempt for the current user')
        self.assertEqual(game.levelattempt.level_number, 1, 'Game should be an attempt at level 1')

    def test_watch_level_too_high(self):
        c = self.login()
        # We cause a warning by using a level too high which is expected
        logging.disable(logging.WARNING)
        response = c.get(reverse('aimmo/watch_level', kwargs={'num': 1000}))
        logging.disable(logging.INFO)
        self.assertEqual(response.status_code, 404)

    def test_watch_inactive_level(self):
        c = self.login()
        self.game.completed = True
        if self.game.is_active:
            self.skipTest('Completed game is active')
        self.game.static_data = '{"test": 1}'
        self.game.save()
        response = c.get(reverse('aimmo/watch', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['active'])
        self.assertEqual(response.context['static_data'], '{"test": 1}')

    def test_games_api(self):
        self.game.main_user = self.user
        self.game.save()
        user2 = User.objects.create_user(username='2', password='password')
        user3 = User.objects.create_user(username='3', password='password')
        models.Avatar(owner=self.user, code=self.CODE, pk=1, game=self.game).save()
        models.Avatar(owner=user2, code='test2', pk=2, game=self.game).save()
        models.Avatar(owner=user3, code='test3', pk=3, game=self.game).save()
        expected = {
            'main': {
                'parameters': [],
                'main_avatar': 1,
                'users': [
                    {
                        'id': 1,
                        'code': self.CODE,
                    },
                    {
                        'id': 2,
                        'code': 'test2',
                    },
                    {
                        'id': 3,
                        'code': 'test3',
                    },
                ]
            }
        }
        c = Client()
        response = c.get(reverse('aimmo/game_details', kwargs={'id': 1}))
        self.assertJSONEqual(response.content, expected)

    def test_games_api_for_non_existant_game(self):
        c = Client()
        response = c.get(reverse('aimmo/game_details', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

    def test_mark_complete(self):
        c = Client()
        response = c.post(reverse('aimmo/complete_game', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Game.objects.get(id=1).completed)

    def test_mark_complete_for_non_existant_game(self):
        c = Client()
        response = c.post(reverse('aimmo/complete_game', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 404)
        self.assertFalse(models.Game.objects.get(id=1).completed)

    def test_mark_complete_requires_POST(self):
        c = Client()
        response = c.get(reverse('aimmo/complete_game', kwargs={'id': 1}))
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(models.Game.objects.get(id=1).completed)

    def test_mark_complete_has_no_csrf_check(self):
        c = Client(enforce_csrf_checks=True)
        response = c.post(reverse('aimmo/complete_game', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Game.objects.get(id=1).completed)

    def test_mark_complete_with_data(self):
        c = Client()
        c.post(reverse('aimmo/complete_game', kwargs={'id': 1}), 'static', content_type='application/json')
        self.assertEqual(models.Game.objects.get(id=1).static_data, 'static')



class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('test', 'test@example.com', 'password')
        cls.user1.save()
        cls.user2 = User.objects.create_user('test2', 'test2@example.com', 'password')
        cls.user2.save()
        cls.game = models.Game(id=1, name='test', public=False)
        cls.game.save()

    def setUp(self):
        self.game.refresh_from_db()

    def test_public_games_can_be_accessed(self):
        self.game.public = True
        self.assertTrue(self.game.can_user_play(self.user1))
        self.assertTrue(self.game.can_user_play(self.user2))

    def test_anon_user_can_play_public_game(self):
        self.game.public = True
        self.assertTrue(self.game.can_user_play(AnonymousUser()))

    def test_authed_user_can_play(self):
        self.game.public = False
        self.game.can_play = [self.user1]
        self.assertTrue(self.game.can_user_play(self.user1))

    def test_non_authed_user_cannot_play(self):
        self.game.public = False
        self.game.can_play = [self.user1]
        self.assertFalse(self.game.can_user_play(self.user2))

    def test_game_active_by_default(self):
        self.assertTrue(self.game.is_active)

    def test_completed_game_inactive(self):
        self.game.completed = True
        self.game.save()
        self.assertFalse(self.game.is_active)
