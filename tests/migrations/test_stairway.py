import pytest
import os

from alembic.config import Config
from alembic.command import downgrade, upgrade
from alembic.script import Script, ScriptDirectory

def get_revisions():
    revisions_dir = ScriptDirectory.from_config(Config(os.getcwd()+"\\alembic.ini"))

    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(revision: Script):
    config = Config(os.getcwd()+"\\alembic.ini")
    upgrade(config, revision.revision)

    downgrade(config, revision.down_revision or "-1")
    upgrade(config, revision.revision)
