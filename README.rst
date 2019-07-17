==============
ORM Benchmarks
==============

**Qualification criteria is:**

* Needs to support minimum 2 databases, e.g. sqlite + something-else
* Runs on Python3.7
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
F. Filter with limit 20 with random offset
G. Get


2) Relational
-------------
TODO



ORMs:
=====

Django:
        https://www.djangoproject.com/

        Pros:

        * Provides all the essential features
        * Simple, clean, API
        * Great test framework
        * Excellent documentation
        * Migrations done right™

        Cons:

        * Brings whole Django along with it

peewee:
        https://github.com/coleifer/peewee


Pony ORM:
        https://github.com/ponyorm/pony

        Pros:

        * Fast
        * Does cacheing automatically

        Cons:

        * Does not support bulk insert.

SQLAlchemy ORM:
        http://www.sqlalchemy.org/

        Pros:

        * The "de facto" ORM in the python world
        * Supports just about every feature and edge case
        * Documentation re DB quirks is second to none

        Cons:

        * Complicated, layers upon layers of leaky abstractions
        * You have to manage transactions manually
        * You have to write a script to get DDL SQL
        * Documentation expects you to be intimate with SQLAlchemy
        * Migrations are add ons

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

Results for SQLite, using the ``SHM`` in-memory filesystem on Linux, to try and make the tests more CPU limited, but still do FS round-trips. Also more consistent than an SSD.

Py37:

==================== ========== ========== ========== ============== ========== ============ ===================
\                    Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM uvloop
==================== ========== ========== ========== ============== ========== ============ ===================
Insert                  6065.39    5645.60    6569.83        2017.10    4145.39     10095.88            12829.76
Insert: atomic          8955.16    7826.12   22403.12       10703.60    5089.01     11271.42            17360.36
Insert: bulk           39260.08   46031.46          —       39850.07          —     50276.71            49200.51
Filter: match          80254.33   46599.65  203517.93       90011.55   24144.28    195661.91           199982.61
Filter: contains       74707.72   44711.45  205796.17       75697.45   21823.63    174481.15           176206.19
Filter: limit 20       31246.21   28035.28  145659.47       33633.12   27496.05     49838.14            54722.05
Get                     3176.05    3627.38   10115.00        2762.78    6668.08      3895.93             4758.92
==================== ========== ========== ========== ============== ========== ============ ===================

PyPy7.1-Py3.6:

===================== ========== ========== ========== ============== ========== ============
\/                    Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
===================== ========== ========== ========== ============== ========== ============
Insert                  5242.25    5451.37    5791.86        1107.91           —     4424.47
Insert: atomic          6722.83    7296.33   19042.90        6942.59           —    19522.18
Insert: bulk           17553.11   24769.06          —       21125.83           —    36688.70
Filter: match         154524.56  105543.11  340737.29      135703.08           —    84318.87
Filter: contains      146560.45  101398.30  368628.43      142638.19           —    82642.94
Filter: limit 20        6835.82   73438.98  197140.48       65193.73           —    41425.38
Get                     4411.47    7846.75    9847.32        4481.98           —     8163.20
===================== ========== ========== ========== ============== ========== ============

Quick analysis
--------------
* Pony ORM is heavily optimised for performance, it wins nearly every metric, and often by a large margin.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is now competitive, especially when using ``uvloop``
* Generally ``uvloop`` provides a modest perf increase.
* ``Get`` is surprisingly slow

PyPy comparison
---------------
* ``peewee`` and ``Pony ORM`` has typically same or better performance
* ``Django`` and ``SQLAlchemy ORM`` has some better, and some worse performance
* ``Tortoise ORM`` has performace wins for atomic inserts and get operations, is significantly slower for large filters.
* ``SQLObject`` fails


Performance of Tortoise
=======================

Versions
--------

Note that these benchmarks have since changed, so state is not exactly the same as above.
This should only be used as a "guideline" of the improvement in performance since we started with the performance optimization process.

==================== ============== ================ ================ ================ ================ ================ ================
Tortoise ORM:        v0.10.6        v0.10.7          v0.10.8          v0.10.9          v0.10.11         v0.11.3          v0.12.1
-------------------- -------------- ---------------- ---------------- ---------------- ---------------- ---------------- ----------------
Seedup (Insert & Big & Small)         19.4, 1.5, 6.1  25.9, 2.0, 6.6    81.8, 2.2, 8.7  95.3, 2.4, 13.1 118.2, 2.7, 14.6 136.9, 2.4, 13.5
=================================== ================ ================ ================ ================ ================ ================
Insert                        89.89          2180.38          2933.19          7635.42          8297.53          9870.59         14544.81
Insert: atomic               149.59          2481.16          3275.53         11966.53         14791.36         18452.56         18245.26
Insert: bulk                      —                —                —                —                —                —         71124.01
Filter: match              55866.14        101035.06        139482.12        158997.41        165398.56        186298.75        160746.73
Filter: contains           76803.14        100536.06        128669.50        142954.66        167127.12        177623.78        159116.08
Filter: limit 20            4583.53         27830.14         29995.23         39170.17         58740.05         65742.82         60285.42
Get                          233.69          1868.15          2136.20          2818.41          4411.01          4899.04          5208.50
==================== ============== ================ ================ ================ ================ ================ ================

Perf issues identified from profiling
-------------------------------------
* No bulk insert operations
* ``base.executor._field_to_db()`` could be replaced with a pre-computed dict lookup
* ``Model.__init__`` is 72% of large queries, and 28% of small queries
* ``Queryset.resolve_filters`` is doing lots of unnecessary stuff, especially for .get() method
* Get operation is slow (likely slow SQL generation, could be resolved with parametrized query cacheing)


On ``tortoise.models.__init__``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``Model.__init__`` is 72% of large queries, and 28% of small queries

The majority of time is spent doing:

* dynamic kwarg handling control flow
* Defaults
* Type conversion/cleanup: ``field_object.to_python_value(value)``.

An experiment indicate a ~10% speedup by pre-generating a closure lookup for type handlers.

Another experiment indicate a ~20% speedup on by skipping ``field_object.to_python_value(value)``

Another experiment with optimal hand-written code gave a ~90% speedup, but there are several issues wit code-generation:

* Error handling should only be done on parameters that are given
* Can generate a function to call to pass parameters in to
* Can't reliably introspect wether to use to_python_value or not

Taking that into account brings effective speedup down to a less impressive ~50%

On Bulk inserts
^^^^^^^^^^^^^^^
Bulk inserts is noticeably faster if inside a transaction.
We can't safely force a transaction around the entire bulk operation, so leave it as is until we have a safe chunking operation.


On Queryset performance
^^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.

Also, we can make more queries use parameterised queries, cache SQL generation, and cache prepared queries.

Perf fixes applied
------------------

1) ``aiosqlite`` **polling misalignment** *(sqlite specific)*

   (20-40% speedup for retrieval, **10-15X** speedup for insertion): https://github.com/jreese/aiosqlite/pull/12
2) ``pypika`` **improved copy implementation** *(generic)*

   (53% speedup for insertion): https://github.com/kayak/pypika/issues/160
3) ``tortoise.models.__init__`` **restructure** *(generic)*

   (25-30% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/51

4) ``tortoise.models.__init__`` **restructure** *(generic)*

   (9-11% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/52

5) ``aiosqlite`` **macros** *(sqlite specific)*

   (1-5% speedup for retrieval, 10-40% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13

6) **Simple prepared insert statements** *(generic)*

   (35-250% speedup for insertion) https://github.com/jreese/aiosqlite/pull/13 https://github.com/tortoise/tortoise-orm/pull/54

7) **pre-generate initial pypika query object per model** *(generic)*

   (25-50% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/54

8) **pre-generate filter map, and standard select for all values per model** *(generic)*

   (15-30% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64

9) **More optimal queryset cloning** *(generic)*

   (6-15% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64

10) ``pypika`` **improved copy implementation** *(generic)*

    (10-15% speedup for small fetch operations) https://github.com/kayak/pypika/pull/205

11) **Optimised inserts/updates & Bulk create** *(generic)*

    | (5-40% speedup for small insert operations)
    | (350-600% speedup for bulk insert over small insert operations) https://github.com/tortoise/tortoise-orm/pull/142

12) **De-lazied some metadata objects** *(generic)*

    (15-25% speedup for large fetch operations)
