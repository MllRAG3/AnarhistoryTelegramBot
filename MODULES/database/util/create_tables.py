from MODULES.database.db_var.archive import ARCHIVE
from MODULES.database.models.users import Authors, Stats
from MODULES.database.models.stories import Stories, Views
from MODULES.database.models.content import Samples, Buttons


def create_world():
    with ARCHIVE:
        ARCHIVE.create_tables([
            Stats,
            Authors,

            Stories,
            Views,

            Samples,
            Buttons,
        ])

    print(['WORLD HAS BEEN CREATED BY GOD -> MIRAGE!'])
