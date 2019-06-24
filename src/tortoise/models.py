from tortoise import fields
from tortoise.models import Model


class Journal(Model):
    timestamp = fields.DatetimeField(auto_now_add=True)
    level = fields.SmallIntField(index=True)
    text = fields.CharField(max_length=255, index=True)
