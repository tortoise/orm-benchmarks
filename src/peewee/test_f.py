import os
import time
from random import randrange

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get('ITERATIONS', '1000')) // 2
start = time.time()


count = 0

for _ in range(iters):
    for level in LEVEL_CHOICE:
        res = list(Journal.select().where(Journal.level == level).limit(20).offset(randrange(int(iters/10))))
        count += len(res)

now = time.time()

print(f'peewee, F: Rows/sec: {count / (now - start): 10.2f}')
