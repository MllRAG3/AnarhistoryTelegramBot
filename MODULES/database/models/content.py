from MODULES.database.models.base_model import BaseModelWithoutLogging
from peewee import CharField, ForeignKeyField, IntegerField


class Samples(BaseModelWithoutLogging):
    text = CharField()
    rows = IntegerField()
    call_when_generated_method_name = CharField()


class Buttons(BaseModelWithoutLogging):
    text = CharField()
    call_data = CharField()
    row = IntegerField()
    content = ForeignKeyField(Samples, backref='buttons')
