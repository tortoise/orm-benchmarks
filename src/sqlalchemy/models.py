from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite3')

Base = declarative_base()


class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    level = Column(SmallInteger, index=True)
    text = Column(String(255), index=True)


def create_tables():
    Base.metadata.create_all(engine)
