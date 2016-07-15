from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from players import models


class TestViews(TestCase):
    CODE = 'class Avatar: pass'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('test', 'test@example.com', 'password')
        cls.user.is_staff = True
        cls.user.save()
        cls.game = models.Game(id=1, name='test')
        cls.game.save()

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

    def test_login_required_for_code(self):
        c = Client()
        response = c.post(reverse('aimmo/program'), {'code': self.CODE})
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

    def test_games_api(self):
        user2 = User.objects.create_user(username='2', password='password')
        user3 = User.objects.create_user(username='3', password='password')
        models.Avatar(owner=self.user, code=self.CODE, pk=1, game=self.game).save()
        models.Avatar(owner=user2, code='test2', pk=2, game=self.game).save()
        models.Avatar(owner=user3, code='test3', pk=3, game=self.game).save()
        expected = {
            'main': {
                'parameters': [],
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


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('test', 'test@example.com', 'password')
        cls.user1.save()
        cls.user2 = User.objects.create_user('test2', 'test2@example.com', 'password')
        cls.user2.save()
        cls.game = models.Game(id=1, name='test', public=False)
        cls.game.save()

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
