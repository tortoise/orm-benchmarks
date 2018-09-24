import os
import time
from random import choice

from models import Journal, conn

LEVEL_CHOICE = [10, 20, 30, 40, 50]

count = int(os.environ.get('ITERATIONS', '1000'))
start = now = time.time()
trans = conn.transaction()
for i in range(count):
    Journal(
        level=choice(LEVEL_CHOICE),
        text=f'Insert from B, item {i}',
        connection=trans
    )
trans.commit(close=True)
now = time.time()

print(f'SQLObject, B: Rows/sec: {count / (now - start): 10.2f}')
