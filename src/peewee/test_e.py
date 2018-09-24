import time

from models import Journal

start = time.time()
count = 0

for _ in range(10):
    for level in ['A', 'B', 'C']:
        res = list(Journal.select().where(Journal.text.contains(f'from {level},')))
        count += len(res)

now = time.time()

print(f'peewee, E: Rows/sec: {count / (now - start): 10.2f}')
