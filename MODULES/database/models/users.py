from MODULES.database.models.base_model import BaseModelWithLogging, BaseModelWithoutLogging
from peewee import CharField, IntegerField, BooleanField, ForeignKeyField


class Stats(BaseModelWithoutLogging):
    respect = IntegerField(default=0)
    views = IntegerField(default=0)


class Authors(BaseModelWithLogging):
    tg_id = IntegerField()
    author_name = CharField(max_length=64, default='Nah, who cares about default values')
    username = CharField(max_length=32)
    is_regged = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    stat = ForeignKeyField(Stats)
