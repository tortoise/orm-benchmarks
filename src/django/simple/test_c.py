import os
import time
from random import choice

import django  # noqa
from simple.models import Journal

django.setup()  # noqa


LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get('ITERATIONS', '1000'))


start = now = time.time()
Journal.objects.bulk_create([
    Journal(
        level=choice(LEVEL_CHOICE),
        text=f'Insert from C, item {i}'
    ) for i in range(count)
])
now = time.time()

print(f'Django, C: Rows/sec: {count / (now - start): 10.2f}')
