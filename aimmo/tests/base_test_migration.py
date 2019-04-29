from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase


class MigrationTestCase(TestCase):
    """A Test case for testing migrations."""

    # These must be defined by subclasses.
    start_migration = None
    dest_migration = None

    django_application = None

    @property
    def app_name(self):
        return apps.get_containing_app_config(type(self).__module__).name

    def setUp(self):
        executor = MigrationExecutor(connection)
        # Migrate to start_migration (the migration before the one you want to test)
        executor.migrate([(self.app_name, self.start_migration)])

        # Rebuild graph. Done between invocations of migrate()
        executor.loader.build_graph()

        # Run the migration you want to test
        executor.migrate([(self.app_name, self.dest_migration)])

        # This application can now be used to get the latest models for testing
        self.django_application = executor.loader.project_state(
            [(self.app_name, self.dest_migration)]
        ).apps
