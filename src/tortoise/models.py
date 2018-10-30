from tortoise import fields
from tortoise.models import Model


class Journal(Model):
    timestamp = fields.DatetimeField(auto_now_add=True)
    level = fields.SmallIntField(db_index=True)
    text = fields.CharField(max_length=255, db_index=True)
