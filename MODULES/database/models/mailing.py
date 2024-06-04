from MODULES.database.models.base_model import BaseModelWithoutLogging
from peewee import CharField, TimeField


class Mailing(BaseModelWithoutLogging):
    message_json = CharField()
    buttons_json = CharField()
    send_time = TimeField()
