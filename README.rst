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
F. Filter with limit 20
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

==================== ========== ========== ========== ============== ========== ============ =====================
\                    Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM (uvloop)
==================== ========== ========== ========== ============== ========== ============ =====================
Insert                  5943.28    5593.84    6900.37        2051.88    3984.26      6877.14               8637.60
Insert: atomic          9256.79    7811.10   25836.91       11938.54    5194.61     10370.12              17227.90
Insert: bulk           40016.98   44411.00          —       50080.17          —            —                     —
Filter: match          78395.50   48285.79  216710.23       98140.48   25307.95    182373.33             185011.74
Filter: contains       78156.17   49013.99  213029.84       89676.78   22544.69    178567.30             179764.66
Filter: limit 20       33153.41   29825.27  397708.52       37618.64   27813.18     55773.37              61700.44
Get                     3159.70    3744.40   10688.77        3033.93    6868.80      3594.64               4363.51
==================== ========== ========== ========== ============== ========== ============ =====================

PyPy7.0-Py3.5:

==================== ========== ========== ========== ============== ========== ============ =====================
\                    Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM (uvloop)
==================== ========== ========== ========== ============== ========== ============ =====================
Insert                  4412.35    5404.36    7591.06        1114.80          —      2946.12               2866.43
Insert: atomic          6558.47    7505.67   24290.22        8741.84          —     14268.02              10056.14
Insert: bulk           18208.38   37460.78          —       25931.92          —            —                     —
Filter: match         157681.98   99918.28  342668.26       96394.91          —     50896.36              50816.38
Filter: contains      161073.25  101175.23  347632.04      109365.11          —     52693.18              52445.68
Filter: limit 20        6496.08   60953.55  563802.67       44450.58          —     25446.42              24254.46
Get                     4010.55    5824.89    9160.72        2529.05          —      3945.98               2937.19
==================== ========== ========== ========== ============== ========== ============ =====================

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
* ``Tortoise ORM`` performs worse in every metric, ``uvloop`` is even worse (as expected)
* ``SQLObject`` fails


Performance of Tortoise
=======================

Versions
--------

==================== ============== ================ ================ ================ ================ ================
Tortoise ORM:        v0.10.6        v0.10.7          v0.10.8          v0.10.9          v0.10.11         v0.11.3
-------------------- -------------- ---------------- ---------------- ---------------- ---------------- ----------------
Seedup (Insert & Big & Small)         19.4, 1.5, 6.1  25.9, 2.0, 6.6    81.8, 2.2, 8.7  95.3, 2.4, 13.1 118.2, 2.7, 14.6
=================================== ================ ================ ================ ================ ================
Insert                        89.89          2180.38          2933.19          7635.42          8297.53          9870.59
Insert: atomic               149.59          2481.16          3275.53         11966.53         14791.36         18452.56
Filter: match              55866.14        101035.06        139482.12        158997.41        165398.56        186298.75
Filter: contains           76803.14        100536.06        128669.50        142954.66        167127.12        177623.78
Filter: limit 20            4583.53         27830.14         29995.23         39170.17         58740.05         65742.82
Get                          233.69          1868.15          2136.20          2818.41          4411.01          4899.04
==================== ============== ================ ================ ================ ================ ================

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

On doing some experiments, optimal hand-written code should be in the realm of 90% faster, so code-generation can fix a lot of this. (Not that interested in doing codegen at this stage)

Another experiment indicate a 10-20% speedup by pre-generating a closure lookup for type handlers.

On Queryset performance
^^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.

Also, we can make more queries use parameterised queries, cache SQL generation, and cache prepared queries.

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

7) **pre-generate initial pypika query object per model** *(generic)*

   (25-50% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/54

8) **pre-generate filter map, and standard select for all values per model** *(generic)*

   (15-30% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64

9) **More optimal queryset cloning** *(generic)*

   (6-15% speedup for small fetch operations) https://github.com/tortoise/tortoise-orm/pull/64

10) **``pypika`` improved copy implementation** *(generic)*

    (10-15% speedup for small fetch operations) https://github.com/kayak/pypika/pull/205
