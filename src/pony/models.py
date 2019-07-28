import os
from datetime import datetime

from pony.orm import Database, Required, Optional, Set

db = Database()

test = int(os.environ.get('TEST', '1'))
if test == 1:
    class Journal(db.Entity):
        timestamp = Required(datetime, default=datetime.now)
        level = Required(int, size=16, index=True)
        text = Required(str, max_len=255, index=True)


if test == 2:
    class Journal(db.Entity):
        timestamp = Required(datetime, default=datetime.now)
        level = Required(int, size=16, index=True)
        text = Required(str, max_len=255, index=True)

        parent = Optional("Journal", reverse="children")
        children = Set("Journal", reverse="parent")
        related = Set("Journal", reverse="related_from")
        related_from = Set("Journal", reverse="related")


db.bind(provider='sqlite', filename='/dev/shm/db.sqlite3', create_db=True)
db.generate_mapping(create_tables=True)
