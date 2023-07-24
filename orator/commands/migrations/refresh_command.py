# -*- coding: utf-8 -*-

from cleo.helpers import option
from .base_command import BaseCommand


class RefreshCommand(BaseCommand):
    """
    Reset and re-run all migrations.

    migrate:refresh
        {--d|database= : The database connection to use.}
        {--p|path= : The path of migrations files to be executed.}
        {--s|seed : Indicates if the seed task should be re-run.}
        {--seed-path= : The path of seeds files to be executed.
                        Defaults to <comment>./seeds</comment>.}
        {--seeder=database_seeder : The name of the root seeder.}
        {--f|force : Force the operation to run.}
    """

    name = "migrate:refresh"
    options = [
        option(
            long_name="database",
            short_name="d",
            description="The database connection to use.",
            flag=False,
        ),
        option(
            long_name="path",
            short_name="p",
            description="The path of migrations files to be executed.",
            flag=False,
        ),
        option(
            long_name="seed",
            short_name="s",
            description="The database connection to use.",
            flag=True,
        ),
        option(
            long_name="seed-path",
            description="The database connection to use.",
            flag=False,
        ),
        option(
            long_name="seeder",
            description="The name of the root seeder.",
            flag=False,
            default="database_seeder",
        ),
        option(
            long_name="force",
            short_name="f",
            description="Force the operation to run.",
            flag=True,
        ),
    ]

    def handle(self):
        """
        Executes the command.
        """
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to refresh the database?:</question> "
        ):
            return

        database = self.option("database")

        options = [("--force", True)]

        if self.option("path"):
            options.append(("--path", self.option("path")))

        if database:
            options.append(("--database", database))

        if self.get_definition().has_option("config"):
            options.append(("--config", self.option("config")))

        self.call("migrate:reset", options)

        self.call("migrate", options)

        if self._needs_seeding():
            self._run_seeder(database)

    def _needs_seeding(self):
        return self.option("seed")

    def _run_seeder(self, database):
        options = [("--seeder", self.option("seeder")), ("--force", True)]

        if database:
            options.append(("--database", database))

        if self.get_definition().has_option("config"):
            options.append(("--config", self.option("config")))

        if self.option("seed-path"):
            options.append(("--path", self.option("seed-path")))

        self.call("db:seed", options)
