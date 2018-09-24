from datetime import datetime

from peewee import CharField, DateTimeField, Model, SmallIntegerField, SqliteDatabase

db = SqliteDatabase('db.sqlite3')


class Journal(Model):
    timestamp = DateTimeField(default=datetime.now)
    level = SmallIntegerField(index=True)
    text = CharField(max_length=255, index=True)

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Journal])
