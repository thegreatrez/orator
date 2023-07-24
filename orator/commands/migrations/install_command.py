# -*- coding: utf-8 -*-

from cleo.helpers import option
from orator.migrations import DatabaseMigrationRepository
from .base_command import BaseCommand


class InstallCommand(BaseCommand):
    """
    Create the migration repository.

    migrate:install
        {--d|database= : The database connection to use.}
    """

    name = "migrate:install"
    options = [
        option(
            long_name="database",
            short_name="d",
            description="The database connection to use.",
            flag=False,
        ),
    ]

    def handle(self):
        """
        Executes the command
        """
        database = self.option("database")
        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        repository.set_source(database)
        repository.create_repository()

        self.info("Migration table created successfully")
