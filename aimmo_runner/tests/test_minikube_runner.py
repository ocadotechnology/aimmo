import logging
import mock
from unittest import TestCase
from aimmo_runner.minikube import create_creator_yaml

logging.basicConfig(level=logging.WARNING)


class TestMinikubeRunner(TestCase):

    @mock.patch('aimmo_runner.minikube.get_ip', return_value='127.0.0.1')
    def test_game_creator_function_creates_correct_game_url(self, mocked_get_ip_func):
        """
        Checks if the game creator yaml is created with the correct game API URL. Relies on get_ip()
        which we expect to fall back to localhost always.
        """
        created_yaml = create_creator_yaml()
        self.assertEqual(created_yaml['spec']['template']['spec']['containers'][0]['env'][1]['value'],
                         'http://127.0.0.1:8000/aimmo/api/games/')
