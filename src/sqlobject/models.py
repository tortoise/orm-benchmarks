from sqlobject import *
from datetime import datetime

conn = sqlhub.processConnection = connectionForURI('sqlite:db.sqlite3')

class Journal(SQLObject):
    timestamp = DateTimeCol(default=datetime.now)
    level = IntCol()
    level_index = DatabaseIndex('level')
    text = StringCol(length=255)
    text_index = DatabaseIndex('text')

