# -*- coding: utf-8 -*-

import os
from cleo.helpers import argument, option
from orator.migrations import MigrationCreator
from .base_command import BaseCommand


class MigrateMakeCommand(BaseCommand):
    """
    Create a new migration file.

    make:migration
        {name : The name of the migration.}
        {--t|table= : The table to create the migration for.}
        {--C|create : Whether the migration will create the table or not.}
        {--p|path= : The path to migrations files.}
    """

    needs_config = False
    name = "make:migration"
    arguments = [
        argument(
            name="name",
            description="The name of the migration.",
        )
    ]
    options = [
        option(
            long_name="table",
            short_name="t",
            description="The table to create the migration for.",
            flag=False,
        ),
        option(
            long_name="create",
            short_name="C",
            description="Whether the migration will create the table or not.",
            flag=True,
        ),
        option(
            long_name="path",
            short_name="p",
            description="The path to migrations files.",
            flag=False,
        ),
    ]

    def handle(self):
        """
        Executes the command.
        """
        creator = MigrationCreator()

        name = self.argument("name")
        table = self.option("table")
        create = bool(self.option("create"))

        if not table and create is not False:
            table = create

        path = self.option("path")
        if path is None:
            path = self._get_migration_path()

        migration_name = self._write_migration(creator, name, table, create, path)

        self.line("<info>Created migration:</info> {}".format(migration_name))

    def _write_migration(self, creator, name, table, create, path):
        """
        Write the migration file to disk.
        """
        file_ = os.path.basename(creator.create(name, path, table, create))

        return file_
