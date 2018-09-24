import time

from models import Journal
from pony.orm import db_session, select

start = time.time()
count = 0

with db_session():
    for _ in range(10):
        for level in ['A', 'B', 'C']:
            res = list(select(j for j in Journal if f'from {level},' in j.text))
            count += len(res)

now = time.time()

print(f'Pony ORM, E: Rows/sec: {count / (now - start): 10.2f}')
