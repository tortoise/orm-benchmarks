from models import Journal, runasync, init
import time
from random import choice
import os


async def runtest():
    await init()

    start = now = time.time()
    count = 0

    for _ in range(10):
        for level in ['A', 'B', 'C']:
            res = list(await Journal.filter(text__contains=f'from {level},').all())
            count += len(res)

    now = time.time()

    print(f'Tortoise ORM, E: Rows/sec: {count / (now - start): 10.2f}')

runasync(runtest())
