from models import db, Journal
import time
from random import choice
import os

LEVEL_CHOICE = [10,20,30,40,50]

count = int(os.environ.get('ITERATIONS', '1000'))
start = now = time.time()
with db.atomic():
    for i in range(count):
        Journal(
            level = choice(LEVEL_CHOICE),
            text = f'Insert from B, item {i}'
        ).save()
now = time.time()

print(f'peewee, B: Rows/sec: {count / (now - start): 10.2f}')

