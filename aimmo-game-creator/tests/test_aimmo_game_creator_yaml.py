import logging
from unittest import TestCase

import yaml

logging.basicConfig(level=logging.WARNING)


class TestAimmoGameCreatorYaml(TestCase):
    def setUp(self):
        with open("rc-aimmo-game-creator.yaml", "r") as stream:
            try:
                self.yaml_dict = yaml.load(stream)
            except yaml.YAMLError as exc:
                logging.debug(exc)

    def test_REPLACE_ME_string_exists(self):
        """
        Ensures the yaml template contains the correct string to be replaced.
        """
        self.assertEqual(
            self.yaml_dict["spec"]["template"]["spec"]["containers"][0]["env"][1][
                "value"
            ],
            "REPLACE_ME",
        )
