from datetime import datetime

from sqlobject import (DatabaseIndex, DateTimeCol, IntCol, SQLObject, StringCol, connectionForURI,
                       sqlhub)

conn = sqlhub.processConnection = connectionForURI('sqlite:/dev/shm/db.sqlite3')


class Journal(SQLObject):
    timestamp = DateTimeCol(default=datetime.now)
    level = IntCol()
    level_index = DatabaseIndex('level')
    text = StringCol(length=255)
    text_index = DatabaseIndex('text')
