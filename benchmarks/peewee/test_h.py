import time

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
start = time.time()


count = 0

for _ in range(10):
    for level in LEVEL_CHOICE:
        res = list(Journal.select().where(Journal.level == level).tuples())
        count += len(res)

now = time.time()

print(f"peewee, H: Rows/sec: {count / (now - start): 10.2f}")
