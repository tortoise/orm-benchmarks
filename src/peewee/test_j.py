import time
from random import choice

from models import Journal, db

LEVEL_CHOICE = [10, 20, 30, 40, 50]



objs = list(Journal.select())
count = len(objs)

start = time.time()

with db.atomic():
    for obj in objs:
        obj.level = choice(LEVEL_CHOICE)
        obj.save(only=['level'])

now = time.time()

print(f'peewee, J: Rows/sec: {count / (now - start): 10.2f}')
