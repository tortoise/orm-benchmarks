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
Insert                      1431.34        1346.74        1790.42        1033.02        1339.64        1282.01
Insert: atomic              8456.38        7410.21       26125.51       10606.63        4960.19        3950.50
Insert: bulk               33924.07       21964.35              —       40889.00              —              —
Filter: match              73072.73       44559.74      234223.27       91469.29       23571.60      167819.65
Filter: contains           64668.07       42089.06      234551.90       87678.00       20985.71      162847.27
Filter: limit 20           30847.96       27522.99      363499.59       36798.24       26713.73       33056.61
Get                         2833.18        3572.36       10621.77        2994.68        6479.70        2221.13
==================== ============== ============== ============== ============== ============== ==============


Performance of Tortoise
=======================

Versions
--------

==================== ============== ============== ============== ============== ==============
Tortoise ORM:        v0.10.6        v0.10.7        v0.10.8a       v0.10.8        latest
-------------------- -------------- -------------- -------------- -------------- --------------
Seedup (Insert & Filter)                12.8 & 1.3     18.2 & 1.9     18.2 & 2.1     22.0 & 2.2
=================================== ============== ============== ============== ==============
Insert                        94.54         977.47        1168.51        1168.51        1282.01
Insert: atomic               143.16        2362.94        3434.66        3434.66        3950.50
Filter: match              67100.22      110509.19      143977.91      156315.69      167819.65
Filter: contains           80936.28      111521.11      138549.93      158048.75      162847.61
==================== ============== ============== ============== ============== ==============

Perf issues identified
----------------------
* No bulk insert operations
* Limit filter is much slower than large filters
* Get operation is slow

On ``pypika`` cpu utilisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now that ``pypika`` has implemented a perf fix for deepcopy, we still want to see if we can avoid using it.

Adding a simple SQL-INSERT cache results in::

    Tortoise ORM, A: Rows/sec:    1759.65
    Tortoise ORM, B: Rows/sec:   13454.37

Which is a significant speedup of 36-260%.
This will require letting SQL driver do the escaping for us.
We would have to do a very similar change to allow bulk inserts to work.

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

5) **``aiosqlite`` macros** *(sqlite specific)* *(not yet reflecting)*

   (1-5% speedup for retrieval, 10-40% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13
