from models import Journal, runasync, init
import time
from random import choice
import os

LEVEL_CHOICE = [10,20,30,40,50]


async def runtest():
    await init()

    start = now = time.time()
    count = 0

    for _ in range(10):
        for level in LEVEL_CHOICE:
            res = list(await Journal.filter(level=level).all())
            count += len(res)

    now = time.time()

    print(f'Tortoise ORM, D: Rows/sec: {count / (now - start): 10.2f}')

runasync(runtest())
