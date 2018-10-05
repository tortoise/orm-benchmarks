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
Insert                      1171.14        1103.92        1050.57         743.95         892.70        1148.99
Insert: atomic              8660.37        6885.19       24232.86       10222.18        4073.83        6881.08
Insert: bulk               33846.46       19532.46              —       39890.63              —              —
Filter: match              75045.46       42126.30      218371.56       82652.81       18369.44      159923.25
Filter: contains           73771.59       41555.80      217527.20       78552.51       18882.55      153463.44
Filter: limit 20           32356.72       22495.73      336676.52       32743.20       25106.52       30905.77
Get                         2913.02        2646.62        8768.91        2830.26        6074.93        1996.00
==================== ============== ============== ============== ============== ============== ==============


Performance of Tortoise
=======================

Versions
--------

==================== ============== ============== ============== ============== ==============
Tortoise ORM:        v0.10.6        v0.10.7        v0.10.8a       v0.10.8        latest
-------------------- -------------- -------------- -------------- -------------- --------------
Seedup (Insert & Filter)                12.8 & 1.3     18.2 & 1.9     18.2 & 2.1     33.6 & 2.1
=================================== ============== ============== ============== ==============
Insert                        94.54         977.47        1168.51        1168.51        1148.99
Insert: atomic               143.16        2362.94        3434.66        3434.66        6881.08
Filter: match              67100.22      110509.19      143977.91      156315.69      159923.25
Filter: contains           80936.28      111521.11      138549.93      158048.75      153463.44
Filter: limit 20                  —              —              —              —       30905.77
Get                               —              —              —              —        1996.00
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
