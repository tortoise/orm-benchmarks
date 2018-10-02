import django  # noqa
django.setup()  # noqa

import os
import time
from random import randint

from simple.models import Journal

count = int(os.environ.get('ITERATIONS', '1000'))
maxval = count - 1
count *= 2
start = time.time()


for _ in range(count):
    Journal.objects.get(id=randint(1, maxval))

now = time.time()

print(f'Django, G: Rows/sec: {count / (now - start): 10.2f}')
