==============
ORM Benchmarks
==============

**Qualification criteria is:**

* Needs to support minimum 2 databases, e.g. sqlite + something-else
* Runs on Python3.6
* Actively developed
* Has ability to generate initial DDL off specified models
* Handle one-to-many relationships


Benchmarks:
===========

These benchmarks are not meant to be used as a direct comparison.
They suffer from co-operative back-off, and is a lot simpler than common real-world scenarios.

1) Single table
---------------

.. code::

    model Journal:
        timestamp: datetime → now()
        level: int(enum) → 10/20/30/40/50
        text: varchar(255) → A selection of text

A. Insert rows (naïve implementation)
B. Insert rows (transactioned)
C. Inster rows (batch)
D. Filter on level
E. Search in text
F. Aggregation
G. Cursor efficiency


2) Relational
-------------
TODO



ORMs:
=====

Django:
        https://www.djangoproject.com/

peewee:
        https://github.com/coleifer/peewee

Pony ORM:
        https://github.com/ponyorm/pony

        * Does not support bulk insert.

SQLAlchemy ORM:
        http://www.sqlalchemy.org/

SQLObject:
        https://github.com/sqlobject/sqlobject

        * Does not support 16-bit integer for ``level``, used 32-bit instead.
        * Does not support bulk insert.

Tortoise ORM:
        https://github.com/tortoise/tortoise-orm

        * Currently the only ``async`` ORM as part of this suite.
        * Does not support bulk insert.

Results (SQLite)
================

==================== ============== ============== ============== ============== ============== ==============
\                    Django         peewee         Pony ORM       SQLAlchemy ORM SQLObject      Tortoise ORM
==================== ============== ============== ============== ============== ============== ==============
Insert                      1163.99        1225.21        1454.15         944.76        1118.88          94.54
Insert: atomic              8476.31        6975.57       24868.60       10234.70        4912.71         143.16
Insert: bulk               34120.59       11528.16              —       38764.79              —              —
Filter: match              68934.47       39307.05      223419.30       75863.22        8140.76       67100.22
Filter: contains           68340.79       39641.32      226013.34       77658.41        5498.24       80936.28
==================== ============== ============== ============== ============== ============== ==============


Perf issues identified
======================
* ``aiosqlite`` will always issue an event loop cycle, whereas changing the blocking call to block the first time only yields significant speed ups (~10-15X for small queries, and even 20-40% for larger queries):

  ==================== ==============
  \                    Tortoise ORM
  ==================== ==============
  Insert                       945.84
  Insert: atomic              2231.41
  Filter: match              94516.01
  Filter: contains           96419.78
  ==================== ==============

  .. code:: py3

    async def _execute(self, fn, *args, **kwargs):
        """Queue a function with the given arguments for execution."""
        await self._lock.acquire()
        pt = partial(fn, *args, **kwargs)
        self._tx.put_nowait(pt)
        try:
            # Many commands return nearly immediately (e.g. in a transaction)
            result = self._rx.get(timeout=0.001)
        except Empty:
            while True:
                try:
                    result = self._rx.get_nowait()
                    break

                except Empty:
                    await asyncio.sleep(0.001)
                    continue

        self._lock.release()
        if isinstance(result, Exception):
            raise result

        return result
