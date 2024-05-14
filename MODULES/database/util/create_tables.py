from MODULES.database.db_var.archive import ARCHIVE

import MODULES.database.models.stories as stories
import MODULES.database.models.users as users
import MODULES.database.models.content as content
import MODULES.database.models.user_history as user_history


def create_world():
    with ARCHIVE:
        ARCHIVE.create_tables([
            stories.Published,
            stories.Drafts,
            stories.Views,

            users.AnonymousSettings,
            users.SearchPreferensies,
            users.Users,

            user_history.UserHistory,

            content.Samples,
            content.Buttons,
        ])

    print(['WORLD HAS BEEN CREATED BY GOD -> MIRAGE!'])
