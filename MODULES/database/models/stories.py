from MODULES.database.models.base_model import BaseModelWithLogging
from MODULES.database.models.users import Authors

from peewee import CharField, BooleanField, ForeignKeyField


class Stories(BaseModelWithLogging):
    title = CharField(max_length=32)
    text = CharField(max_length=4096)
    is_active = BooleanField(default=True)
    author = ForeignKeyField(Authors, backref='stories')


class Views(BaseModelWithLogging):
    story = ForeignKeyField(Stories)
    user = ForeignKeyField(Authors, backref='watched')
