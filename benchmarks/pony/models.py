import os
from datetime import datetime
from decimal import Decimal

from pony.orm import Database, Required, Optional, Set, LongUnicode, Json

db = Database()

test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(db.Entity):
        timestamp = Required(datetime, default=datetime.now)
        level = Required(int, size=16, index=True)
        text = Required(str, max_len=255, index=True)


if test == 2:

    class Journal(db.Entity):
        timestamp = Required(datetime, default=datetime.now)
        level = Required(int, size=16, index=True)
        text = Required(str, max_len=255, index=True)

        parent = Optional("Journal", reverse="children")
        children = Set("Journal", reverse="parent")
        related = Set("Journal", reverse="related_from")
        related_from = Set("Journal", reverse="related")


if test == 3:

    class Journal(db.Entity):
        timestamp = Required(datetime, default=datetime.now)
        level = Required(int, size=16, index=True)
        text = Required(str, max_len=255, index=True)

        col_float1 = Required(float, default=2.2)
        col_smallint1 = Required(int, size=16, default=2)
        col_int1 = Required(int, size=32, default=2000000)
        col_bigint1 = Required(int, size=64, default=99999999)
        col_char1 = Required(str, max_len=255, default="value1")
        col_text1 = Required(
            LongUnicode, default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal1 = Required(Decimal, 12, 8, default=Decimal("2.2"))
        col_json1 = Required(
            Json, default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float2 = Optional(float)
        col_smallint2 = Optional(int, size=16)
        col_int2 = Optional(int, size=32)
        col_bigint2 = Optional(int, size=64)
        col_char2 = Optional(str, max_len=255)
        col_text2 = Optional(LongUnicode)
        col_decimal2 = Optional(Decimal, 12, 8)
        col_json2 = Optional(Json)

        col_float3 = Required(float, default=2.2)
        col_smallint3 = Required(int, size=16, default=2)
        col_int3 = Required(int, size=32, default=2000000)
        col_bigint3 = Required(int, size=64, default=99999999)
        col_char3 = Required(str, max_len=255, default="value1")
        col_text3 = Required(
            LongUnicode, default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal3 = Required(Decimal, 12, 8, default=Decimal("2.2"))
        col_json3 = Required(
            Json, default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float4 = Optional(float)
        col_smallint4 = Optional(int, size=16)
        col_int4 = Optional(int, size=32)
        col_bigint4 = Optional(int, size=64)
        col_char4 = Optional(str, max_len=255)
        col_text4 = Optional(LongUnicode)
        col_decimal4 = Optional(Decimal, 12, 8)
        col_json4 = Optional(Json)


dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    db.bind(
        provider="postgres",
        user="postgres",
        password=os.environ.get('PASSWORD'),
        host="127.0.0.1",
        database="tbench",
    )
elif dbtype == "mysql":
    db.bind(provider="mysql", host="127.0.0.1", user="root", passwd=os.environ.get('PASSWORD'), db="tbench")
else:
    db.bind(provider="sqlite", filename="/dev/shm/db.sqlite3", create_db=True)

db.generate_mapping(create_tables=True)
