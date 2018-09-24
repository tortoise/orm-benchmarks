import time

from models import Journal
from sqlobject.sqlbuilder import CONTAINSSTRING

start = time.time()
count = 0

for _ in range(10):
    for level in ['A', 'B', 'C']:
        res = list(Journal.select(CONTAINSSTRING(Journal.q.text, f'from {level},')))
        count += len(res)

now = time.time()

print(f'SQLObject, E: Rows/sec: {count / (now - start): 10.2f}')
