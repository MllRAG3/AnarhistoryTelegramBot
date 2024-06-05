from playhouse.migrate import *
from MODULES.database.db_var.archive import ARCHIVE

migrator = SqliteMigrator(ARCHIVE)

migrate(
    migrator.drop_column('stories', 'title'),
    migrator.drop_column('stories', 'text'),
    migrator.drop_column('stories', 'is_active'),
    migrator.add_column('stories', 'json', CharField(max_length=4096, null='{}')),
    migrator.add_column('stories', 'type', CharField(max_length=32, null='text')),
)
