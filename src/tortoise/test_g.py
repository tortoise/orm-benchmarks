import os
import time

from models import Journal, init

from tortoise import run_async
from random import randint

count = int(os.environ.get('ITERATIONS', '1000'))
maxval = count - 1
count *= 2


async def runtest():
    await init()

    start = now = time.time()

    for _ in range(count):
        await Journal.get(id=randint(1, maxval))

    now = time.time()

    print(f'Tortoise ORM, G: Rows/sec: {count / (now - start): 10.2f}')

run_async(runtest())
