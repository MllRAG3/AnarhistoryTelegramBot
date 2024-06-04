from playhouse.migrate import *
from MODULES.database.db_var.archive import ARCHIVE

migrator = SqliteMigrator(ARCHIVE)

migrate(
    migrator.add_column('mailing', 'type', CharField(null='text'))
)
