import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:////dev/shm/db.sqlite3')

Base = declarative_base()

test = int(os.environ.get('TEST', '1'))
if test == 1:
    class Journal(Base):
        __tablename__ = 'journal'

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now)
        level = Column(SmallInteger, index=True)
        text = Column(String(255), index=True)


if test == 2:
    class JournalRelated(Base):
        __tablename__ = 'journal_related'
        journal_id = Column(Integer, ForeignKey('journal.id'), primary_key=True)
        journal_from_id = Column(Integer, ForeignKey('journal.id'), primary_key=True)


    class Journal(Base):
        __tablename__ = 'journal'

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now)
        level = Column(SmallInteger, index=True)
        text = Column(String(255), index=True)
        parent_id = Column(Integer, ForeignKey('journal.id'))
        parent = relationship("Journal", remote_side=id, backref="children")
        related = relationship('JournalRelated',backref='to', primaryjoin=id==JournalRelated.journal_id)
        related_from = relationship('JournalRelated',backref='from', primaryjoin=id==JournalRelated.journal_from_id)


def create_tables():
    Base.metadata.create_all(engine)
