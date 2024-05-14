from peewee import Model, AutoField, DateTimeField
from datetime import datetime

from MODULES.database.db_var.archive import ARCHIVE


class BaseModelWithLogging(Model):
    id = AutoField()

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(BaseModelWithLogging, self).save(*args, **kwargs)

    class Meta:
        database = ARCHIVE


class BaseModelWithoutLogging(Model):
    id = AutoField()

    class Meta:
        database = ARCHIVE
