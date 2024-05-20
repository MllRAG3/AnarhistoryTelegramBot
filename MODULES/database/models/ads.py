from MODULES.database.models.base_model import BaseModelWithoutLogging
from peewee import IntegerField, CharField, BooleanField


class Ads(BaseModelWithoutLogging):
    text = CharField(max_length=4096)
    pic = CharField()
    show_time = IntegerField()
    HTML_format = BooleanField()
