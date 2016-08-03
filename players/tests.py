from django.contrib.auth.models import User
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

    def login(self):
        c = Client()
        c.login(username='test', password='password')
        return c

    def test_add_new_code(self):
        c = self.login()
        response = c.post(reverse('aimmo/code'), {'code': self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Player.objects.get(user__username='test').code, self.CODE)

    def test_update_code(self):
        c = self.login()
        models.Player(user=self.user, code='test').save()
        response = c.post(reverse('aimmo/code'), {'code': self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Player.objects.get(user__username='test').code, self.CODE)

    def test_login_required_for_code(self):
        c = Client()
        response = c.post(reverse('aimmo/program'), {'code': self.CODE})
        self.assertNotEqual(response.status_code, 200)

    def test_default_code(self):
        c = self.login()
        response = c.get(reverse('aimmo/code'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith('class Avatar'))

    def test_retrieve_code(self):
        models.Player(user=self.user, code=self.CODE).save()
        c = self.login()
        response = c.get(reverse('aimmo/code'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.CODE)

    def test_games_api(self):
        user2 = User.objects.create_user(username='2', password='password')
        user3 = User.objects.create_user(username='3', password='password')
        models.Player(user=self.user, code=self.CODE, pk=1).save()
        models.Player(user=user2, code='test2', pk=2).save()
        models.Player(user=user3, code='test3', pk=3).save()
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
        response = c.get(reverse('aimmo/games'))
        self.assertJSONEqual(response.content, expected)
