import os
from datetime import datetime
from decimal import Decimal

from sqlobject import (
    DatabaseIndex,
    DateTimeCol,
    IntCol,
    SQLObject,
    connectionForURI,
    sqlhub,
    ForeignKey,
    RelatedJoin,
    MultipleJoin,
    FloatCol,
    UnicodeCol,
    DecimalCol,
    JSONCol,
)

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    conn = sqlhub.processConnection = connectionForURI(
        "postgres://postgres@localhost/tbench"
    )
elif dbtype == "mysql":
    conn = sqlhub.processConnection = connectionForURI("mysql://root:@localhost/tbench")
else:
    conn = sqlhub.processConnection = connectionForURI("sqlite:/dev/shm/db.sqlite3")

test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(SQLObject):
        timestamp = DateTimeCol(default=datetime.now, notNone=True)
        level = IntCol(notNone=True)
        level_index = DatabaseIndex("level")
        text = UnicodeCol(length=255, notNone=True)
        text_index = DatabaseIndex("text")


if test == 2:

    class Journal(SQLObject):
        timestamp = DateTimeCol(default=datetime.now, notNone=True)
        level = IntCol(notNone=True)
        level_index = DatabaseIndex("level")
        text = UnicodeCol(length=255, notNone=True)
        text_index = DatabaseIndex("text")

        parent = ForeignKey("Journal", default=None)
        children = MultipleJoin("Journal")
        related = RelatedJoin(
            "Journal", joinColumn="journal_id", otherColumn="journal_from_id"
        )
        related_from = RelatedJoin(
            "Journal",
            joinColumn="journal_from_id",
            otherColumn="journal_id",
            createRelatedTable=False,
        )


if test == 3:

    class Journal(SQLObject):
        timestamp = DateTimeCol(default=datetime.now, notNone=True)
        level = IntCol(notNone=True)
        level_index = DatabaseIndex("level")
        text = UnicodeCol(length=255, notNone=True)
        text_index = DatabaseIndex("text")

        col_float1 = FloatCol(default=2.2, notNone=True)
        col_smallint1 = IntCol(default=2, notNone=True)
        col_int1 = IntCol(default=2000000, notNone=True)
        col_bigint1 = IntCol(default=99999999, notNone=True)
        col_char1 = UnicodeCol(length=255, default="value1", notNone=True)
        col_text1 = UnicodeCol(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa", notNone=True
        )
        col_decimal1 = DecimalCol(
            size=12, precision=8, default=Decimal("2.2"), notNone=True
        )
        col_json1 = JSONCol(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}, notNone=True
        )

        col_float2 = FloatCol(default=None)
        col_smallint2 = IntCol(default=None)
        col_int2 = IntCol(default=None)
        col_bigint2 = IntCol(default=None)
        col_char2 = UnicodeCol(length=255, default=None)
        col_text2 = UnicodeCol(default=None)
        col_decimal2 = DecimalCol(size=12, precision=8, default=None)
        col_json2 = JSONCol(default=None)
