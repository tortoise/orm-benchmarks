import os
import time
from random import randint

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get('ITERATIONS', '1000'))
maxval = count - 1
count *= 2
start = time.time()


for _ in range(count):
    val = randint(1, maxval)
    Journal.get(Journal.id == val)

now = time.time()

print(f'peewee, F: Rows/sec: {count / (now - start): 10.2f}')
