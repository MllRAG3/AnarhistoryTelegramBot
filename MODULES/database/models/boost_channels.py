from MODULES.database.models.base_model import BaseModelWithoutLogging
from peewee import CharField, IntegerField


class BoostChannels(BaseModelWithoutLogging):
    link = CharField()
    tid = IntegerField()
    boost = IntegerField()
