import os
from datetime import datetime
from decimal import Decimal
from typing import ForwardRef, Optional

import databases
import ormar
import sqlalchemy

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    DATABASE_URL = f"postgresql://postgres:{os.environ.get('PASSWORD')}@localhost:{os.environ.get('PGPORT', '5432')}/tbench"
elif dbtype == "mysql":
    DATABASE_URL = f"mysql://root:{os.environ.get('PASSWORD')}@127.0.0.1:{os.environ.get('MYPORT', '3306')}/tbench"
else:
    DATABASE_URL = "sqlite:////tmp/db.sqlite3"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

base_ormar_config = ormar.OrmarConfig(
    metadata=metadata,
    database=database,
)

test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(ormar.Model):
        ormar_config = base_ormar_config.copy(tablename="journal")

        id: int = ormar.Integer(primary_key=True)
        timestamp: datetime = ormar.DateTime(default=datetime.now)
        level: int = ormar.SmallInteger(index=True)
        text: str = ormar.String(max_length=255, index=True)


if test == 2:

    class Journal(ormar.Model):
        ormar_config = base_ormar_config.copy(tablename="journal")

        id: int = ormar.Integer(primary_key=True)
        timestamp: datetime = ormar.DateTime(default=datetime.now)
        level: int = ormar.SmallInteger(index=True)
        text: str = ormar.String(max_length=255, index=True)
        parent: Optional[ForwardRef("Journal")] = ormar.ForeignKey(
            ForwardRef("Journal"), related_name="children", nullable=True
        )

    Journal.update_forward_refs()


if test == 3:

    class Journal(ormar.Model):
        ormar_config = base_ormar_config.copy(tablename="journal")

        id: int = ormar.Integer(primary_key=True)
        timestamp: datetime = ormar.DateTime(default=datetime.now)
        level: int = ormar.SmallInteger(index=True)
        text: str = ormar.String(max_length=255, index=True)

        col_float1: float = ormar.Float(default=2.2)
        col_smallint1: int = ormar.SmallInteger(default=2)
        col_int1: int = ormar.Integer(default=2000000)
        col_bigint1: int = ormar.BigInteger(default=99999999)
        col_char1: str = ormar.String(max_length=255, default="value1")
        col_text1: str = ormar.Text(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal1: Decimal = ormar.Decimal(
            max_digits=12, decimal_places=8, default=Decimal("2.2")
        )
        col_json1: dict = ormar.JSON(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float2: Optional[float] = ormar.Float(nullable=True)
        col_smallint2: Optional[int] = ormar.SmallInteger(nullable=True)
        col_int2: Optional[int] = ormar.Integer(nullable=True)
        col_bigint2: Optional[int] = ormar.BigInteger(nullable=True)
        col_char2: Optional[str] = ormar.String(max_length=255, nullable=True)
        col_text2: Optional[str] = ormar.Text(nullable=True)
        col_decimal2: Optional[Decimal] = ormar.Decimal(
            max_digits=12, decimal_places=8, nullable=True
        )
        col_json2: Optional[dict] = ormar.JSON(nullable=True)

        col_float3: float = ormar.Float(default=2.2)
        col_smallint3: int = ormar.SmallInteger(default=2)
        col_int3: int = ormar.Integer(default=2000000)
        col_bigint3: int = ormar.BigInteger(default=99999999)
        col_char3: str = ormar.String(max_length=255, default="value1")
        col_text3: str = ormar.Text(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal3: Decimal = ormar.Decimal(
            max_digits=12, decimal_places=8, default=Decimal("2.2")
        )
        col_json3: dict = ormar.JSON(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float4: Optional[float] = ormar.Float(nullable=True)
        col_smallint4: Optional[int] = ormar.SmallInteger(nullable=True)
        col_int4: Optional[int] = ormar.Integer(nullable=True)
        col_bigint4: Optional[int] = ormar.BigInteger(nullable=True)
        col_char4: Optional[str] = ormar.String(max_length=255, nullable=True)
        col_text4: Optional[str] = ormar.Text(nullable=True)
        col_decimal4: Optional[Decimal] = ormar.Decimal(
            max_digits=12, decimal_places=8, nullable=True
        )
        col_json4: Optional[dict] = ormar.JSON(nullable=True)


def create_tables():
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
    engine.dispose()
