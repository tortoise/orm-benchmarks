from models import *
import time
import os
import math

LEVEL_CHOICE = [10,20,30,40,50]

start = time.time()
count = 0

with db_session():
    for _ in range(10):
        for level in LEVEL_CHOICE:
            res = list(select(j for j in Journal if j.level == level))
            count += len(res)

now = time.time()

print(f'Pony ORM, D: Rows/sec: {count / (now - start): 10.2f}')
