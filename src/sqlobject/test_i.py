import time
from random import choice

from models import Journal, conn

LEVEL_CHOICE = [10, 20, 30, 40, 50]

trans = conn.transaction()
objs = list(Journal.select(connection=trans))
count = len(objs)
start = time.time()

for obj in objs:
    obj.level = choice(LEVEL_CHOICE)
    obj.text = f'{obj.text} Update'
trans.commit(close=True)

now = time.time()

print(f'SQLObject, I: Rows/sec: {count / (now - start): 10.2f}')
