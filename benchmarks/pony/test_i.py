import time
from random import choice

from models import Journal
from pony.orm import commit, db_session, select

LEVEL_CHOICE = [10, 20, 30, 40, 50]


with db_session():
    objs = list(select(j for j in Journal))
    count = len(objs)

    start = time.time()

    for obj in objs:
        obj.level = choice(LEVEL_CHOICE)
        obj.text = f"{obj.text} Update"
    commit()

    now = time.time()

print(f"Pony ORM, I: Rows/sec: {count / (now - start): 10.2f}")
