from playhouse.migrate import *
from MODULES.database.db_var.archive import ARCHIVE

migrator = SqliteMigrator(ARCHIVE)

migrate(
    migrator.rename_column('boostchannels', 'boost', 'amount')
)
