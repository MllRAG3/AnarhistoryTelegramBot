from MODULES.database.models.base_model import BaseModelWithLogging
from peewee import CharField, IntegerField, BooleanField, ForeignKeyField


class AnonymousSettings(BaseModelWithLogging):
    """
    True - анонимно
    False - не анонимно
    """
    profile = BooleanField(default=True)
    subscriptions = BooleanField(default=True)


class SearchPreferensies(BaseModelWithLogging):
    show_authors = BooleanField(default=True)
    show_authors_n = IntegerField(default=2)
    show_stories_by_title = BooleanField(default=True)
    show_stories_by_title_n = IntegerField(default=2)
    show_stories_by_text = BooleanField(default=True)
    show_stories_by_text_n = IntegerField(default=5)


class Users(BaseModelWithLogging):
    tg_id = IntegerField()
    author_name = CharField(max_length=64, default='Nah, who cares about default values')
    username = CharField(max_length=32)

    rating = IntegerField(default=0)
    is_author = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    anonymous = ForeignKeyField(AnonymousSettings)
    search = ForeignKeyField(SearchPreferensies)
