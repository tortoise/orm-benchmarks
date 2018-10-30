import os
import time

import django  # noqa
from simple.models import Journal

django.setup()  # noqa


LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get('ITERATIONS', '1000')) // 2
start = time.time()


count = 0

for _ in range(10):
    for level in LEVEL_CHOICE:
        res = list(Journal.objects.filter(level=level).all()[:20])
        count += len(res)

now = time.time()

print(f'Django, F: Rows/sec: {count / (now - start): 10.2f}')
