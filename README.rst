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
Insert                      1541.33        1636.39        1723.31        1046.88        1398.05        1168.51
Insert: atomic              8606.80        7195.57       25081.35       10807.63        5028.46        3434.66
Insert: bulk               34608.04       16296.22              —       41225.71              —              —
Filter: match              77777.10       44015.95      236084.81       91546.02       23209.64      156315.69
Filter: contains           74965.12       43531.28      229073.64       87644.81       20781.49      158048.75
==================== ============== ============== ============== ============== ============== ==============


Performance of Tortoise
=======================

Perf issues identified
----------------------
* No bulk insert operations
* Transactioned inserts ``pypika`` CPU utilisation. Whilst improved still the slowest.
* ``tortoise.models.__init__`` → investigate something more efficient than if-elif-elif-elif

On ``pypika`` cpu utilisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now that ``pypika`` has implemented a perf fix for deepcopy, we still want to see if we can avoid using it.

Adding a very naïve SQL cache results in::

  Tortoise ORM, A: Rows/sec:    1696.85
  Tortoise ORM, B: Rows/sec:    5703.24

Which is a significant speedup. Also there is a lot on unnesseccary work being done, in ``_prepare_insert_values()`` and ``_prepare_insert_columns()`` that can be cached as well, etc..
This will require letting SQL driver do the escaping for us (which would be preferred, as it would allow their own optimisations to happen). This would require a large restructure.
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
