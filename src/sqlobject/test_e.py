import os
import time

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get('ITERATIONS', '1000'))

start = time.time()
count = 0

for _ in range(iters // 10):
    for level in LEVEL_CHOICE:
        res = list(Journal.select(Journal.q.level == level).limit(20))
        count += len(res)

now = time.time()

print(f'SQLObject, E: Rows/sec: {count / (now - start): 10.2f}')
