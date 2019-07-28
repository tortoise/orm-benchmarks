import os
from datetime import datetime

from peewee import CharField, DateTimeField, Model, SmallIntegerField, SqliteDatabase, ForeignKeyField

db = SqliteDatabase('/dev/shm/db.sqlite3')

test = int(os.environ.get('TEST', '1'))
if test == 1:
    class Journal(Model):
        timestamp = DateTimeField(default=datetime.now)
        level = SmallIntegerField(index=True)
        text = CharField(max_length=255, index=True)

        class Meta:
            database = db

if test == 2:
    class Journal(Model):
        timestamp = DateTimeField(default=datetime.now)
        level = SmallIntegerField(index=True)
        text = CharField(max_length=255, index=True)
        parent = ForeignKeyField('self', null=True, backref='children')

        class Meta:
            database = db

    class JournalRelated(Model):
        journal_id = ForeignKeyField(Journal, backref='related')
        journal_from_id = ForeignKeyField(Journal, backref='related_from')


def create_tables():
    with db:
        db.create_tables([Journal])
