import os
import sys
from decimal import Decimal

from piccolo.columns import (
    BigInt,
    DoublePrecision,
    ForeignKey,
    Integer,
    JSONB,
    Numeric,
    SmallInt,
    Text,
    Timestamp,
    Varchar,
)
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.table import Table

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    from piccolo.engine.postgres import PostgresEngine

    DB = PostgresEngine(
        config={
            "host": "127.0.0.1",
            "port": int(os.environ.get("PGPORT", "5432")),
            "database": "tbench",
            "user": "postgres",
            "password": os.environ.get("PASSWORD", ""),
        }
    )
elif dbtype == "mysql":
    sys.exit(0)
else:
    from piccolo.engine.sqlite import SQLiteEngine

    DB = SQLiteEngine(path="/tmp/db.sqlite3")

test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(Table, db=DB):
        timestamp = Timestamp(default=TimestampNow())
        level = SmallInt(index=True)
        text = Varchar(length=255, index=True)


if test == 2:

    class Journal(Table, db=DB):
        timestamp = Timestamp(default=TimestampNow())
        level = SmallInt(index=True)
        text = Varchar(length=255, index=True)
        parent = ForeignKey(references="self", null=True, default=None)


if test == 3:

    class Journal(Table, db=DB):
        timestamp = Timestamp(default=TimestampNow())
        level = SmallInt(index=True)
        text = Varchar(length=255, index=True)

        col_float1 = DoublePrecision(default=2.2)
        col_smallint1 = SmallInt(default=2)
        col_int1 = Integer(default=2000000)
        col_bigint1 = BigInt(default=99999999)
        col_char1 = Varchar(length=255, default="value1")
        col_text1 = Text(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal1 = Numeric(digits=(12, 8), default=Decimal("2.2"))
        col_json1 = JSONB(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float2 = DoublePrecision(null=True, default=None)
        col_smallint2 = SmallInt(null=True, default=None)
        col_int2 = Integer(null=True, default=None)
        col_bigint2 = BigInt(null=True, default=None)
        col_char2 = Varchar(length=255, null=True, default=None)
        col_text2 = Text(null=True, default=None)
        col_decimal2 = Numeric(digits=(12, 8), null=True, default=None)
        col_json2 = JSONB(null=True, default=None)

        col_float3 = DoublePrecision(default=2.2)
        col_smallint3 = SmallInt(default=2)
        col_int3 = Integer(default=2000000)
        col_bigint3 = BigInt(default=99999999)
        col_char3 = Varchar(length=255, default="value1")
        col_text3 = Text(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal3 = Numeric(digits=(12, 8), default=Decimal("2.2"))
        col_json3 = JSONB(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float4 = DoublePrecision(null=True, default=None)
        col_smallint4 = SmallInt(null=True, default=None)
        col_int4 = Integer(null=True, default=None)
        col_bigint4 = BigInt(null=True, default=None)
        col_char4 = Varchar(length=255, null=True, default=None)
        col_text4 = Text(null=True, default=None)
        col_decimal4 = Numeric(digits=(12, 8), null=True, default=None)
        col_json4 = JSONB(null=True, default=None)
