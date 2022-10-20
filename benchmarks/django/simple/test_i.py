try:
    import django  # noqa

    django.setup()  # noqa
finally:
    pass

import time
from random import choice

from simple.models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]

objs = Journal.objects.all()
count = len(objs)

start = time.time()
for obj in objs:
        obj.level = choice(LEVEL_CHOICE)
        obj.text = f"{obj.text} Update"

Journal.objects.bulk_update(objs, ['level', 'text'])
now = time.time()

print(f"Django, I: Rows/sec: {count / (now - start): 10.2f}")
