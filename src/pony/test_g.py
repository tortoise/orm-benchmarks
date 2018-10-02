import os
import time
from random import randint

from models import Journal
from pony.orm import db_session, select


count = int(os.environ.get('ITERATIONS', '1000'))
maxval = count - 1
count *= 2
start = time.time()


with db_session():
    for _ in range(count):
        val = randint(1, maxval)
        select(j for j in Journal if j.id == val).get()

now = time.time()

print(f'Pony ORM, G: Rows/sec: {count / (now - start): 10.2f}')
