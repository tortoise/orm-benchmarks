import os
import time
from random import choice

from models import Journal, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))


Session = sessionmaker(bind=engine)
session = Session()

objs = list(session.query(Journal).all())
count = len(objs)

start = time.time()

for obj in objs:
    session.delete(obj)
session.commit()

now = time.time()

print(f"SQLAlchemy ORM, K: Rows/sec: {count / (now - start): 10.2f}")
