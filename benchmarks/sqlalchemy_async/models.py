import os
from datetime import datetime
from decimal import Decimal

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
from sqlalchemy.orm import declarative_base, relationship

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

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(Base):
        __tablename__ = "journal"

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now, nullable=False)
        level = Column(SmallInteger, index=True, nullable=False)
        text = Column(String(255), index=True, nullable=False)


if test == 2:

    class JournalRelated(Base):
        __tablename__ = "journal_related"
        journal_id = Column(Integer, ForeignKey("journal.id"), primary_key=True)
        journal_from_id = Column(Integer, ForeignKey("journal.id"), primary_key=True)

    class Journal(Base):
        __tablename__ = "journal"

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now, nullable=False)
        level = Column(SmallInteger, index=True, nullable=False)
        text = Column(String(255), index=True, nullable=False)
        parent_id = Column(Integer, ForeignKey("journal.id"))
        parent = relationship("Journal", remote_side="Journal.id", backref="children")
        related = relationship(
            "JournalRelated", backref="to", primaryjoin="Journal.id == JournalRelated.journal_id"
        )
        related_from = relationship(
            "JournalRelated",
            backref="from_journal",
            primaryjoin="Journal.id == JournalRelated.journal_from_id",
        )


if test == 3:

    class Journal(Base):
        __tablename__ = "journal"

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now, nullable=False)
        level = Column(SmallInteger, index=True, nullable=False)
        text = Column(String(255), index=True, nullable=False)

        col_float1 = Column(Float, default=2.2, nullable=False)
        col_smallint1 = Column(SmallInteger, default=2, nullable=False)
        col_int1 = Column(Integer, default=2000000, nullable=False)
        col_bigint1 = Column(BigInteger, default=99999999, nullable=False)
        col_char1 = Column(String(255), default="value1", nullable=False)
        col_text1 = Column(
            Text,
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
            nullable=False,
        )
        col_decimal1 = Column(Numeric(12, 8), default=Decimal("2.2"), nullable=False)
        col_json1 = Column(
            JSON,
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
            nullable=False,
        )

        col_float2 = Column(Float)
        col_smallint2 = Column(SmallInteger)
        col_int2 = Column(Integer)
        col_bigint2 = Column(BigInteger)
        col_char2 = Column(String(255))
        col_text2 = Column(Text)
        col_decimal2 = Column(Numeric(12, 8))
        col_json2 = Column(JSON)

        col_float3 = Column(Float, default=2.2, nullable=False)
        col_smallint3 = Column(SmallInteger, default=2, nullable=False)
        col_int3 = Column(Integer, default=2000000, nullable=False)
        col_bigint3 = Column(BigInteger, default=99999999, nullable=False)
        col_char3 = Column(String(255), default="value1", nullable=False)
        col_text3 = Column(
            Text,
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
            nullable=False,
        )
        col_decimal3 = Column(Numeric(12, 8), default=Decimal("2.2"), nullable=False)
        col_json3 = Column(
            JSON,
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
            nullable=False,
        )

        col_float4 = Column(Float)
        col_smallint4 = Column(SmallInteger)
        col_int4 = Column(Integer)
        col_bigint4 = Column(BigInteger)
        col_char4 = Column(String(255))
        col_text4 = Column(Text)
        col_decimal4 = Column(Numeric(12, 8))
        col_json4 = Column(JSON)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
