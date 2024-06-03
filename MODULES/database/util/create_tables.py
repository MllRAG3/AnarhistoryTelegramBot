from MODULES.database.db_var.archive import ARCHIVE
from MODULES.database.models.users import Authors, Stats
from MODULES.database.models.stories import Stories, Views
from MODULES.database.models.content import Samples, Buttons
from MODULES.database.models.mailing import Mailing
from MODULES.database.models.boost_channels import BoostChannels


def create_world():
    """
    Создает все таблицы ы базе данных
    :return:
    """
    with ARCHIVE:
        ARCHIVE.create_tables([
            Stats,
            Authors,

            Stories,
            Views,

            Samples,
            Buttons,

            Mailing,
            BoostChannels,
        ])

    print(['WORLD HAS BEEN CREATED BY GOD -> MIRAGE!'])
