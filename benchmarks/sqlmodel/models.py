import os
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    engine = create_async_engine(
        f"postgresql+asyncpg://postgres:{os.environ.get('PASSWORD')}@localhost:{os.environ.get('PGPORT', '5432')}/tbench"
    )
elif dbtype == "mysql":
    engine = create_async_engine(
        f"mysql+aiomysql://root:{os.environ.get('PASSWORD')}@localhost:{os.environ.get('MYPORT', '3306')}/tbench"
    )
else:
    engine = create_async_engine("sqlite+aiosqlite:////tmp/db.sqlite3")

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        timestamp: datetime = Field(
            default_factory=datetime.now,
            sa_column=Column(DateTime, nullable=False, default=datetime.now),
        )
        level: int = Field(sa_column=Column(SmallInteger, index=True, nullable=False))
        text: str = Field(sa_column=Column(String(255), index=True, nullable=False))


if test == 2:

    class JournalRelated(SQLModel, table=True):
        __tablename__ = "journal_related"
        journal_id: int = Field(
            sa_column=Column(Integer, ForeignKey("journal.id"), primary_key=True)
        )
        journal_from_id: int = Field(
            sa_column=Column(Integer, ForeignKey("journal.id"), primary_key=True)
        )

    class Journal(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        timestamp: datetime = Field(
            default_factory=datetime.now,
            sa_column=Column(DateTime, nullable=False, default=datetime.now),
        )
        level: int = Field(sa_column=Column(SmallInteger, index=True, nullable=False))
        text: str = Field(sa_column=Column(String(255), index=True, nullable=False))
        parent_id: Optional[int] = Field(default=None, foreign_key="journal.id")


if test == 3:

    class Journal(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        timestamp: datetime = Field(
            default_factory=datetime.now,
            sa_column=Column(DateTime, nullable=False, default=datetime.now),
        )
        level: int = Field(sa_column=Column(SmallInteger, index=True, nullable=False))
        text: str = Field(sa_column=Column(String(255), index=True, nullable=False))

        col_float1: float = Field(default=2.2, sa_column=Column(Float, default=2.2, nullable=False))
        col_smallint1: int = Field(default=2, sa_column=Column(SmallInteger, default=2, nullable=False))
        col_int1: int = Field(default=2000000, sa_column=Column(Integer, default=2000000, nullable=False))
        col_bigint1: int = Field(
            default=99999999, sa_column=Column(BigInteger, default=99999999, nullable=False)
        )
        col_char1: str = Field(
            default="value1", sa_column=Column(String(255), default="value1", nullable=False)
        )
        col_text1: str = Field(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
            sa_column=Column(
                Text,
                default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
                nullable=False,
            ),
        )
        col_decimal1: Decimal = Field(
            default=Decimal("2.2"),
            sa_column=Column(Numeric(12, 8), default=Decimal("2.2"), nullable=False),
        )
        col_json1: dict = Field(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
            sa_column=Column(
                JSON,
                default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
                nullable=False,
            ),
        )

        col_float2: Optional[float] = Field(default=None, sa_column=Column(Float))
        col_smallint2: Optional[int] = Field(default=None, sa_column=Column(SmallInteger))
        col_int2: Optional[int] = Field(default=None, sa_column=Column(Integer))
        col_bigint2: Optional[int] = Field(default=None, sa_column=Column(BigInteger))
        col_char2: Optional[str] = Field(default=None, sa_column=Column(String(255)))
        col_text2: Optional[str] = Field(default=None, sa_column=Column(Text))
        col_decimal2: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 8)))
        col_json2: Optional[dict] = Field(default=None, sa_column=Column(JSON))

        col_float3: float = Field(default=2.2, sa_column=Column(Float, default=2.2, nullable=False))
        col_smallint3: int = Field(default=2, sa_column=Column(SmallInteger, default=2, nullable=False))
        col_int3: int = Field(default=2000000, sa_column=Column(Integer, default=2000000, nullable=False))
        col_bigint3: int = Field(
            default=99999999, sa_column=Column(BigInteger, default=99999999, nullable=False)
        )
        col_char3: str = Field(
            default="value1", sa_column=Column(String(255), default="value1", nullable=False)
        )
        col_text3: str = Field(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
            sa_column=Column(
                Text,
                default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
                nullable=False,
            ),
        )
        col_decimal3: Decimal = Field(
            default=Decimal("2.2"),
            sa_column=Column(Numeric(12, 8), default=Decimal("2.2"), nullable=False),
        )
        col_json3: dict = Field(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
            sa_column=Column(
                JSON,
                default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
                nullable=False,
            ),
        )

        col_float4: Optional[float] = Field(default=None, sa_column=Column(Float))
        col_smallint4: Optional[int] = Field(default=None, sa_column=Column(SmallInteger))
        col_int4: Optional[int] = Field(default=None, sa_column=Column(Integer))
        col_bigint4: Optional[int] = Field(default=None, sa_column=Column(BigInteger))
        col_char4: Optional[str] = Field(default=None, sa_column=Column(String(255)))
        col_text4: Optional[str] = Field(default=None, sa_column=Column(Text))
        col_decimal4: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 8)))
        col_json4: Optional[dict] = Field(default=None, sa_column=Column(JSON))


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
