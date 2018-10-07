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
F. Filter with limit 20
G. Get


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
Insert                      1553.57        1651.90        1937.00        1042.08        1353.27        2014.71
Insert: atomic              8672.27        6690.74       26892.96       11031.48        4934.03       14052.90
Insert: bulk               34327.99       17854.72              —       42179.58              —              —
Filter: match              77871.60       43615.76      231521.96       95877.78       23712.88      166211.40
Filter: contains           75387.23       43338.21      240953.01       90177.86       21903.76      160933.64
Filter: limit 20           32671.26       27783.54      366764.49       36529.24       26849.95       32052.33
Get                         2971.37        3488.66       10797.08        2978.16        6457.87        1998.98
==================== ============== ============== ============== ============== ============== ==============


Performance of Tortoise
=======================

Versions
--------

==================== ============== ============== ============== ==============
Tortoise ORM:        v0.10.6        v0.10.7        v0.10.8        branch
-------------------- -------------- -------------- -------------- --------------
Seedup (Insert & Filter)                12.8 & 1.3     18.2 & 2.1     67.5 & 2.2
=================================== ============== ============== ==============
Insert                        94.54         977.47        1168.51        2014.71
Insert: atomic               143.16        2362.94        3434.66       14052.90
Filter: match              67100.22      110509.19      156315.69      166211.40
Filter: contains           80936.28      111521.11      158048.75      160933.64
Filter: limit 20                  —              —              —       32052.33
Get                               —              —              —        1998.98
==================== ============== ============== ============== ==============

Perf issues identified
----------------------
* No bulk insert operations
* Limit filter is much slower than large filters (seems DB limited, except for Pony ORM)
* Get operation is slow (possibly CPU limited)

On ``pypika`` performance
^^^^^^^^^^^^^^^^^^^^^^^^^
Pypika is unfortunately quite slow, but it does provide guarantees of immutability that we can use to speed up query generation.
e.g. partially build query, and then re-use it later on.

On ``tortoise.models.__init__``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The majority of time is spent doing type conversion/cleanup: ``field_object.to_python_value(value)``.
This is something that is correct, so I deem it fine as is, and we don't try to make it run any faster right now.
Besides, we are second fastest for these metrics.


Perf fixes applied
------------------

1) **``aiosqlite`` polling misalignment** *(sqlite specific)*

   (20-40% speedup for retrieval, **10-15X** speedup for insertion): https://github.com/jreese/aiosqlite/pull/12
2) **``pypika`` improved copy implementation** *(generic)*

   (53% speedup for insertion): https://github.com/kayak/pypika/issues/160
3) **``tortoise.models.__init__`` restructure** *(generic)*

   (25-30% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/51

4) **``tortoise.models.__init__`` restructure** *(generic)*

   (9-11% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/52

5) **``aiosqlite`` macros** *(sqlite specific)*

   (1-5% speedup for retrieval, 10-40% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13

6) **Simple prepared insert statements** *(generic)*

   (35-250% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13 https://github.com/tortoise/tortoise-orm/pull/54
