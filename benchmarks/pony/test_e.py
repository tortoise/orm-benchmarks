import os
import time
from random import randrange

from models import Journal
from pony.orm import db_session, select

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get("ITERATIONS", "1000"))
start = time.time()


count = 0

with db_session():
    for _ in range(iters // 10):
        for level in LEVEL_CHOICE:
            res = list(
                select(j for j in Journal if j.level == level).limit(
                    20, randrange(iters - 20)
                )
            )
            count += len(res)

now = time.time()

print(f"Pony ORM, E: Rows/sec: {count / (now - start): 10.2f}")
