import logging
from unittest import TestCase

import yaml

from kube_components import TokenSecretCreator


class TestKubeComponents(TestCase):
    def setUp(self):
        secret_creator = TokenSecretCreator()
        self.template = secret_creator.load_template(
            "TEST_NAME", "TEST_NAMESPACE", {"token": "TEST_TOKEN"}
        )

    def test_template_is_loaded_and_data_is_added_correctly(self):
        """
        Ensures the yaml template contains the correct string to be replaced.
        """
        self.assertIsNotNone(self.template["metadata"])
        self.assertIsNotNone(self.template["data"])
        self.assertEqual(self.template["metadata"]["name"], "TEST_NAME")
        self.assertEqual(self.template["metadata"]["namespace"], "TEST_NAMESPACE")
        self.assertEqual(self.template["data"]["token"], "TEST_TOKEN")
