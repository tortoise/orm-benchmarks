import json
import os
from datetime import datetime
from decimal import Decimal

from peewee import (
    BigIntegerField,
    CharField,
    DateTimeField,
    DecimalField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    MySQLDatabase,
    SmallIntegerField,
    TextField,
)
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.sqlite_ext import SqliteExtDatabase

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    db = PostgresqlExtDatabase("tbench", user="postgres", password=os.environ.get("PASSWORD"))
elif dbtype == "mysql":
    db = MySQLDatabase("tbench", user="root", password=os.environ.get("PASSWORD"))
else:
    db = SqliteExtDatabase(
        "/tmp/db.sqlite3",
        pragmas=(("journal_mode", "wal"),),  # Use WAL-mode (you should always use this!).
    )


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


test = int(os.environ.get("TEST", "1"))
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
        parent = ForeignKeyField("self", null=True, backref="children")

        class Meta:
            database = db

    class JournalRelated(Model):
        journal_id = ForeignKeyField(Journal, backref="related")
        journal_from_id = ForeignKeyField(Journal, backref="related_from")


if test == 3:

    class Journal(Model):
        timestamp = DateTimeField(default=datetime.now)
        level = SmallIntegerField(index=True)
        text = CharField(max_length=255, index=True)

        col_float1 = FloatField(default=2.2)
        col_smallint1 = SmallIntegerField(default=2)
        col_int1 = IntegerField(default=2000000)
        col_bigint1 = BigIntegerField(default=99999999)
        col_char1 = CharField(max_length=255, default="value1")
        col_text1 = TextField(default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa")
        col_decimal1 = DecimalField(12, 8, default=Decimal("2.2"))
        col_json1 = JSONField(default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True})

        col_float2 = FloatField(null=True)
        col_smallint2 = SmallIntegerField(null=True)
        col_int2 = IntegerField(null=True)
        col_bigint2 = BigIntegerField(null=True)
        col_char2 = CharField(max_length=255, null=True)
        col_text2 = TextField(null=True)
        col_decimal2 = DecimalField(12, 8, null=True)
        col_json2 = JSONField(null=True)

        col_float3 = FloatField(default=2.2)
        col_smallint3 = SmallIntegerField(default=2)
        col_int3 = IntegerField(default=2000000)
        col_bigint3 = BigIntegerField(default=99999999)
        col_char3 = CharField(max_length=255, default="value1")
        col_text3 = TextField(default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa")
        col_decimal3 = DecimalField(12, 8, default=Decimal("2.2"))
        col_json3 = JSONField(default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True})

        col_float4 = FloatField(null=True)
        col_smallint4 = SmallIntegerField(null=True)
        col_int4 = IntegerField(null=True)
        col_bigint4 = BigIntegerField(null=True)
        col_char4 = CharField(max_length=255, null=True)
        col_text4 = TextField(null=True)
        col_decimal4 = DecimalField(12, 8, null=True)
        col_json4 = JSONField(null=True)

        class Meta:
            database = db


def create_tables():
    with db:
        db.create_tables([Journal])
