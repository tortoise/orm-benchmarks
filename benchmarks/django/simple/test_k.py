try:
    import django  # noqa

    django.setup()  # noqa
finally:
    pass

import time
from random import choice

from django.db import transaction
from simple.models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]


objs = list(Journal.objects.all())
count = len(objs)

start = time.time()

with transaction.atomic():
    for obj in objs:
        obj.delete()

now = time.time()

print(f"Django, K: Rows/sec: {count / (now - start): 10.2f}")
