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

Tests:
------

A. Insert: Single (single entry at a time)
B. Insert: Batch (many batched in a transaction)
C. Insert: Bulk (using bulk insert operations)
D. Filter: Large (a large result set)
E. Filter: Small (a limit 20 with random offset)
F. Get
G. Filter: dict
H. Filter: tuple
I. Update: Whole (update the whole object)
J. Update: Partial (update only a single field of the whole object)
K. Delete


1) Small table, no relations
----------------------------

.. code::

    model Journal:
        id: autonumber primary key
        timestamp: datetime → now()
        level: small int(enum) → 10/20/30/40/50 (indexed)
        text: varchar(255) → A selection of text (indexed)


2) Small table, with relations
------------------------------

.. code::

    model Journal:
        id: autonumber primary key
        timestamp: datetime → now()
        level: small int(enum) → 10/20/30/40/50 (indexed)
        text: varchar(255) → A selection of text (indexed)

        parent: FK to parent BigTree
        child: reverse-FB to parent BigTree
        knows: M2M to BigTree


3) Large table
--------------

.. code::

    model BigTree:
        id: uuid primary key
        created_at: datetime → initial-now()
        updated_at: datetime → always-now()
        level: small int(enum) → 10/20/30/40/50 (indexed)
        text: varchar(255) → A selection of text (indexed)

        # Repeated 2 times with defaults, another 2 times as optional:
        col_float: double
        col_smallint: small integer
        col_int: integer
        col_bigint: big integer
        col_char: char(255)
        col_text: text
        col_decimal: decimal(12,8)
        col_json: json


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
        * Documentation re DB quirks is excellent

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
        * Disclaimer: I'm an active contributor to this project


Results (SQLite)
================

Results for SQLite, using the ``SHM`` in-memory filesystem on Linux, to try and make the tests more CPU limited, but still do FS round-trips. Also more consistent than an SSD.

Py37:

=============== ========== ========== ========== ============== ========== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     6317.55    6887.34    6505.66        2065.64    4394.21     13364.75
Insert: Batch      9027.21    7584.29   22673.63       10574.05    5787.25     18186.44
Insert: Bulk      40075.98   47522.73          —       39701.42          —     50464.53
Filter: Large     79445.42   46462.73  206051.20       90559.47   27459.44    212050.91
Filter: Small     31179.32   28900.99  148072.40       33350.18   30457.35     60784.16
Get                3154.31    3789.94   10286.93        2738.42    7104.77      6151.10
Filter: dict     116927.90   68816.43  114768.16       93311.25          —    313948.59
Filter: tuple    124359.26   66897.54  206750.86      355825.32          —    308538.03
Update: Whole      4592.00    6105.88   26171.07       20632.06   13413.61     20651.34
Update: Partial    4963.62    8197.81   37326.12       30671.62   27656.09     23571.15
Delete             5684.04   12211.04   55330.80       56920.03    5432.65     26604.16
Geometric Mean    16971.35   17056.61   47573.13       28085.77   11493.56     44076.92
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     5917.12    6730.08    5427.61        1713.82    4161.41     13324.82
Insert: Batch      8159.04    7575.02   14621.10        8006.42    5237.04     17723.91
Insert: Bulk      34193.66   45657.46          —       39025.97          —     45068.45
Filter: Large     76850.27   41305.82  190535.30       85320.45   26649.25    188235.43
Filter: Small     28063.99   25939.28  140991.14       30955.80   30140.80     57892.99
Get                2989.02    3437.84   10282.67        2501.26    6735.42      6042.80
Filter: dict     115925.18   62251.57  100346.77       87957.53          —    280611.82
Filter: tuple    121190.93   62244.85  189147.41      325820.53          —    269768.91
Update: Whole      4310.54    5268.01   23306.60       11499.54   13548.28     19967.81
Update: Partial    4822.90    8406.46   30771.52       14645.08   27750.82     24287.89
Delete              898.24   12055.36   25639.10         560.90    3697.52     27367.26
Geometric Mean     13534.6   16011.88   38758.74       15139.48   10637.15     41929.43
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     2887.51    2706.10    3124.89        1555.69    2168.91      7569.24
Insert: Batch      3338.14    2836.43    5260.97        4935.80    2465.98      8924.89
Insert: Bulk       5953.94    7625.00          —       17844.05          —     15227.32
Filter: Large     25540.46   14900.14   51151.17       28043.62   12869.16     23678.19
Filter: Small     13449.23    9844.98   63883.50       12663.18   13649.02     18399.23
Get                1437.03    1177.15    5802.84         986.79    3691.46      2235.45
Filter: dict      32532.41   23278.43   20152.74       21838.25          —     30074.90
Filter: tuple     35202.79   24822.37   50943.52       47746.16          —     31693.25
Update: Whole      2696.80    1435.15   18327.27       13814.61   12089.34      9640.19
Update: Partial    4543.57    8307.97   23618.52       17177.39   24101.25     22162.51
Delete             4928.12   12249.64   40242.69       32736.68    3458.30     25406.81
Geometric Mean     6994.09    6484.86   18820.22        11314.2    6575.42     14317.73
=============== ========== ========== ========== ============== ========== ============


PyPy7.1-Py3.6:

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     5100.06    5382.76    5821.95         850.12      4073.14
Insert: Batch      6085.54    5795.74   16253.72        6723.15     17022.11
Insert: Bulk      15433.46   20533.54          —       17157.52     35640.39
Filter: Large    137513.37   91247.73  295651.16      112271.85     73931.75
Filter: Small      5938.01   68236.34  181106.78       50010.01     35448.50
Get                3422.89    7695.80    8606.52        3872.18      7302.07
Filter: dict     124002.51  104283.60  213993.03      101032.31     77670.27
Filter: tuple    146486.98  115928.94  333009.32      194792.29    102366.01
Update: Whole      6776.48   17727.31   38186.83       21819.21      5938.21
Update: Partial    7811.37   21461.86   50689.33       35892.04      8789.32
Delete             8330.27   26346.55   64110.59       73565.18     11283.21
Geometric Mean    15295.94   26031.61   57361.16       25031.38     20142.36
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4614.75    5067.40    5408.42         768.09      3900.72
Insert: Batch      6187.52    5865.57   13889.78        5255.67     16263.25
Insert: Bulk      15047.94   20948.41          —       18065.37     29301.21
Filter: Large    119424.47   87229.47  292587.76      106208.97     56582.93
Filter: Small      4921.75   64822.41  168048.53       49482.60     30196.86
Get                3547.09    7387.87    8473.93        3832.67      5788.82
Filter: dict     119909.32  106676.99  224871.30       96005.86     66080.11
Filter: tuple    138177.10  118731.74  328496.49      187744.75     91382.99
Update: Whole      6532.66   16871.93   33912.03       16715.71      4836.89
Update: Partial    7240.48   22744.50   40385.16       24061.22      9781.47
Delete             2280.56   31114.15   36869.58         605.89     10363.30
Geometric Mean    12867.44   26164.25   50900.85       14605.57     17730.31
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2487.11    3357.77    3591.84         685.06      2787.74
Insert: Batch      2866.41    3566.03    6855.89        4374.36      7146.71
Insert: Bulk       4540.41    7654.51          —       13363.68     13210.44
Filter: Large     22633.88   28656.02  115716.11       31701.85      2711.80
Filter: Small      1864.65   22945.16   99144.99       21644.99      2358.22
Get                2074.13    4210.58    7032.85        1948.50      1234.74
Filter: dict      24740.76   33379.94   79424.08       25089.98      2778.87
Filter: tuple     26859.81   39489.67  107007.57       43747.41      8675.65
Update: Whole      3876.02    6431.08   27576.05       12200.27      1224.01
Update: Partial    6446.09   17087.90   31143.89       14992.91      5617.92
Delete             7804.06   26761.37   49095.95       66105.89      7779.73
Geometric Mean      6006.5   12310.04   30566.76       11951.53      3840.44
=============== ========== ========== ========== ============== ============



Quick analysis
--------------
* Pony ORM is heavily optimised for performance, it wins nearly every metric, and often by a large margin.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is competitive.
* ``Get`` is surprisingly slow for everyone.
* Pony ORM, SQLAlchemy & SQLObject does merge operations for updates, so is technically always partial updates.

PyPy comparison
---------------
* ``peewee`` and ``Pony ORM`` gets a noticeable performance improvement
* ``SQLAlchemy ORM`` is marginally faster
* ``Django`` and ``Tortoise ORM`` is typically slower
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

   (20-40% speedup for retrieval, **10× — 15×** speedup for insertion): https://github.com/jreese/aiosqlite/pull/12
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

12) **De-lazied some metadata objects & More efficient queryset manipulation** *(generic)*

    | (15-25% speedup for large fetch operations)
    | (5-30% speedup for small fetches) https://github.com/tortoise/tortoise-orm/pull/158

13) **Parametrized delete/update** *(generic)*

    | (260-280% speedup for delete operations)
    | (300-600% speedup for update operations) https://github.com/tortoise/tortoise-orm/pull/177

14) **Lazy Relation properties** *(generic)*

    (15~140% speedup for all on Test 2 (Small & Relational)) https://github.com/tortoise/tortoise-orm/pull/187
