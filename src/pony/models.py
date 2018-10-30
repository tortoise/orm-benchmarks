from datetime import datetime

from pony.orm import Database, Required

db = Database()


class Journal(db.Entity):
    timestamp = Required(datetime, default=datetime.now)
    level = Required(int, size=16)
    text = Required(str, max_len=255)


db.bind(provider='sqlite', filename='/dev/shm/db.sqlite3', create_db=True)
db.generate_mapping(create_tables=True)
