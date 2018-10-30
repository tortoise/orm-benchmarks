#!/usr/bin/env python
import sys

DESC = {
    'A': 'Insert',
    'B': 'Insert:\xa0atomic',
    'C': 'Insert:\xa0bulk',
    'D': 'Filter:\xa0match',
    'E': 'Filter:\xa0contains',
    'F': 'Filter:\xa0limit\xa020',
    'G': 'Get',
}

val = sys.stdin.read()
vals = [text.strip() for text in val.strip().split('\n') if text]

data = {}
tests = set()

for bench in vals:
    orm = bench.split(',')[0].strip()
    test = bench.split(',')[1].split(':')[0].strip()
    ops = bench.split(':')[2].strip()
    data.setdefault(orm, {})[test] = ops
    tests.add(test)

tests = sorted(list(tests))
groups = sorted(data.keys(), key=lambda s: s.lower())
lens = [max(len(text), 10) for text in groups]
titles = [f"\{'':19}"] + [f"{group:{_len}}" for group, _len in zip(groups, lens)]  # noqa

print('')
print(' '.join(['=' * len(text) for text in titles]))
print(' '.join(titles).rstrip())
print(' '.join(['=' * len(text) for text in titles]))

for test in tests:
    results = [f'{DESC[test]:20}']
    for group, _len in zip(groups, lens):
        results.append(f"{data[group].get(test, '—'):>{_len}}")
    print(' '.join(results).rstrip())

print(' '.join(['=' * len(text) for text in titles]))
