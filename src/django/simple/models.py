from django.db import models


class Journal(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.SmallIntegerField(db_index=True)
    text = models.CharField(max_length=255, db_index=True)
