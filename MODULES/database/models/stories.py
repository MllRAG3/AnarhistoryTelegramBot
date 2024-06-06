from MODULES.database.models.base_model import BaseModelWithLogging
from MODULES.database.models.users import Authors

from peewee import CharField, ForeignKeyField


class Stories(BaseModelWithLogging):
    author = ForeignKeyField(Authors, backref='stories')
    json = CharField(max_length=4096)
    type = CharField(max_length=32)


class Views(BaseModelWithLogging):
    story = ForeignKeyField(Stories)
    user = ForeignKeyField(Authors, backref='watched')
