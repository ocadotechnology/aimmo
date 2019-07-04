import logging
from unittest import TestCase

import yaml

from kube_components import TokenSecretCreator


class TestKubeComponents(TestCase):
    def setUp(self):
        secret_creator = TokenSecretCreator
        self.secret = secret_creator.create_secret_object(
            None, "game-1-token", "default", {"token": "TEST_TOKEN"}
        )

    def test_secret_is_loaded_and_data_is_added_correctly(self):
        """
        Ensures the secret object is created correctly with the correct data filled in.
        """
        self.assertIsNotNone(self.secret.metadata)
        self.assertIsNotNone(self.secret.string_data)
        self.assertEqual(self.secret.metadata.name, "game-1-token")
        self.assertEqual(self.secret.metadata.namespace, "default")
        self.assertEqual(self.secret.string_data["token"], "TEST_TOKEN")
