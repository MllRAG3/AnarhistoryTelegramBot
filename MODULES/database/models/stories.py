from MODULES.database.models.base_model import BaseModelWithLogging
from MODULES.database.models.users import Users

from peewee import CharField, BooleanField, ForeignKeyField, IntegerField


class Drafts(BaseModelWithLogging):
    title = CharField(max_length=32)
    text = CharField(max_length=4096)
    author = ForeignKeyField(Users, backref='drafts')


class Published(BaseModelWithLogging):
    title = CharField(max_length=32)
    text = CharField(max_length=4096)
    rating = IntegerField(default=0)
    protected = BooleanField(default=False)
    author = ForeignKeyField(Users, backref='published')


class Views(BaseModelWithLogging):
    user = ForeignKeyField(Users, backref='stories_seen')
    story = ForeignKeyField(Published, backref='views')
