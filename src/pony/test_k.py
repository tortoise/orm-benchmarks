import time
from random import choice

from models import Journal
from pony.orm import db_session, select, commit

LEVEL_CHOICE = [10, 20, 30, 40, 50]


with db_session():
    objs = list(select(j for j in Journal))
    count = len(objs)

    start = time.time()

    for obj in objs:
        obj.delete()
    commit()

    now = time.time()

print(f'Pony ORM, K: Rows/sec: {count / (now - start): 10.2f}')
