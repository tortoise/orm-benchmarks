import time
from random import choice

from models import Journal, db

LEVEL_CHOICE = [10, 20, 30, 40, 50]


objs = list(Journal.select())
count = len(objs)

start = time.time()

with db.atomic():
    for obj in objs:
        obj.delete_instance()

now = time.time()

print(f"peewee, K: Rows/sec: {count / (now - start): 10.2f}")
