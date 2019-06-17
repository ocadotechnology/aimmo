import logging
from unittest import TestCase

import yaml

from kube_components import TokenSecretCreator


class TestKubeComponents(TestCase):
    def setUp(self):
        secret_creator = TokenSecretCreator
        self.secret = secret_creator.create_secret_object(
            None, "TEST_NAME", "TEST_NAMESPACE", {"token": "TEST_TOKEN"}
        )

    def test_secret_is_loaded_and_data_is_added_correctly(self):
        """
        Ensures the yaml secret contains the correct string to be replaced.
        """
        self.assertIsNotNone(self.secret.metadata)
        self.assertIsNotNone(self.secret.string_data)
        self.assertEqual(self.secret.metadata.name, "TEST_NAME")
        self.assertEqual(self.secret.metadata.namespace, "TEST_NAMESPACE")
        self.assertEqual(self.secret.string_data["token"], "TEST_TOKEN")
