import os

from tortoise import fields
from tortoise.models import Model

test = int(os.environ.get('TEST', '1'))
if test == 1:
    class Journal(Model):
        timestamp = fields.DatetimeField(auto_now_add=True)
        level = fields.SmallIntField(index=True)
        text = fields.CharField(max_length=255, index=True)


if test == 2:
    class Journal(Model):
        timestamp = fields.DatetimeField(auto_now_add=True)
        level = fields.SmallIntField(index=True)
        text = fields.CharField(max_length=255, index=True)
        parent = fields.ForeignKeyField('models.Journal', related_name='children', null=True)
        related = fields.ManyToManyField('models.Journal', related_name='related_from')
