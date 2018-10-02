import os
import time

from models import Journal, init

from tortoise import run_async

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get('ITERATIONS', '1000')) // 2


async def runtest():
    await init()

    start = now = time.time()
    count = 0

    for _ in range(iters):
        for level in LEVEL_CHOICE:
            res = list(await Journal.filter(level=level).limit(20))
            count += len(res)

    now = time.time()

    print(f'Tortoise ORM, F: Rows/sec: {count / (now - start): 10.2f}')

run_async(runtest())
