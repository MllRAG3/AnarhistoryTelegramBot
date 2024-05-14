from MODULES.database.models.base_model import BaseModelWithLogging
from MODULES.database.models.users import Users
from peewee import ForeignKeyField, CharField


class UserHistory(BaseModelWithLogging):
    page_name = CharField()
    user = ForeignKeyField(Users, backref='history')
