from MODULES.database.models.base_model import BaseModelWithoutLogging
from peewee import CharField, ForeignKeyField, IntegerField, BooleanField


class Samples(BaseModelWithoutLogging):
    text = CharField()
    rows = IntegerField()
    main_button = BooleanField()


class Buttons(BaseModelWithoutLogging):
    text = CharField()
    call_data = CharField()
    row = IntegerField()
    content = ForeignKeyField(Samples, backref='buttons')
