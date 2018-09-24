import django  # noqa
django.setup()  # noqa

import time

from simple.models import Journal

start = time.time()
count = 0

for _ in range(10):
    for level in ['A', 'B', 'C']:
        res = list(Journal.objects.filter(text__icontains=f'from {level},').all())
        count += len(res)

now = time.time()

print(f'Django, E: Rows/sec: {count / (now - start): 10.2f}')
