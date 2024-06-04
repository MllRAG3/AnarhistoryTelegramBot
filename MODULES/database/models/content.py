from MODULES.database.models.base_model import BaseModelWithoutLogging
from peewee import CharField


class Samples(BaseModelWithoutLogging):
    type = CharField()
    message_json = CharField()
    markup_json = CharField()
