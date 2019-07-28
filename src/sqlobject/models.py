import os
from datetime import datetime

from sqlobject import (DatabaseIndex, DateTimeCol, IntCol, SQLObject, StringCol, connectionForURI,
                       sqlhub, ForeignKey, RelatedJoin, MultipleJoin)

conn = sqlhub.processConnection = connectionForURI('sqlite:/dev/shm/db.sqlite3')

test = int(os.environ.get('TEST', '1'))
if test == 1:
    class Journal(SQLObject):
        timestamp = DateTimeCol(default=datetime.now)
        level = IntCol()
        level_index = DatabaseIndex('level')
        text = StringCol(length=255)
        text_index = DatabaseIndex('text')


if test == 2:
    class Journal(SQLObject):
        timestamp = DateTimeCol(default=datetime.now)
        level = IntCol()
        level_index = DatabaseIndex('level')
        text = StringCol(length=255)
        text_index = DatabaseIndex('text')

        parent = ForeignKey('Journal', default=None)
        children = MultipleJoin('Journal')
        related = RelatedJoin('Journal', joinColumn='journal_id', otherColumn='journal_from_id')
        related_from = RelatedJoin('Journal', joinColumn='journal_from_id', otherColumn='journal_id', createRelatedTable=False)

