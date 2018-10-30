import os
import time
from random import randint

from models import Journal

count = int(os.environ.get('ITERATIONS', '1000'))
maxval = count - 1
count *= 2


async def runtest(loopstr):
    start = now = time.time()

    for _ in range(count):
        await Journal.get(id=randint(1, maxval))

    now = time.time()

    print(f'Tortoise ORM{loopstr}, G: Rows/sec: {count / (now - start): 10.2f}')
