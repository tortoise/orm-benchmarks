import os
from django.db import models


class Journal1(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.SmallIntegerField(db_index=True)
    text = models.CharField(max_length=255, db_index=True)

class Journal2(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.SmallIntegerField(db_index=True)
    text = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey('Journal2', related_name='children', on_delete=models.CASCADE, null=True)
    related = models.ManyToManyField('Journal2', related_name='related_from')


test = int(os.environ.get('TEST', '1'))
if test == 1:
    Journal = Journal1
if test == 2:
    Journal = Journal2
