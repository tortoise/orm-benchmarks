from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.ext.indexable import index_property

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

