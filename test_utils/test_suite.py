import unittest
import importlib
import logging

from django.test.runner import DiscoverRunner
import django.conf


LOGGER = logging.getLogger(__name__)


class DjangoAutoTestSuite(unittest.TestSuite):
    """
    This test suite configures django settings (which should be in test_settings.py), and starts a test runner.
    It allows us to run the django tests with setup.py test.
    """

    def __init__(self, *args, **kwargs):
        self._configure()
        self.test_runner = DiscoverRunner()
        tests = self.test_runner.build_suite()
        super(DjangoAutoTestSuite, self).__init__(tests=tests, *args, **kwargs)
        self.test_runner.setup_test_environment()

        self.test_dbs = self.test_runner.setup_databases()

    def _configure(self):
        test_settings = importlib.import_module('test_settings')
        setting_attrs = {attr: getattr(test_settings, attr) for attr in dir(test_settings) if '__' not in attr}

        if not django.conf.settings.configured:
            django.conf.settings.configure(**setting_attrs)

        django.setup()

    def run(self, result_obj, *args, **kwargs):
        result = super(DjangoAutoTestSuite, self).run(result_obj, *args, **kwargs)
        self.test_runner.teardown_databases(self.test_dbs)
        self.test_runner.teardown_test_environment()

        return result
