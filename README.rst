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
Insert: Single     6317.55    6887.34    6505.66        2065.64    4394.21     13185.69
Insert: Batch      9027.21    7584.29   22673.63       10574.05    5787.25     17349.28
Insert: Bulk      40075.98   47522.73          —       39701.42          —     48521.99
Filter: Large     79445.42   46462.73  206051.20       90559.47   27459.44    257240.51
Filter: Small     31179.32   28900.99  148072.40       33350.18   30457.35     63610.04
Get                3154.31    3789.94   10286.93        2738.42    7104.77      6359.75
Filter: dict     116927.90   68816.43  114768.16       93311.25          —    327541.99
Filter: tuple    124359.26   66897.54  206750.86      355825.32          —    314446.94
Update: Whole      4592.00    6105.88   26171.07       20632.06   13413.61     20903.99
Update: Partial    4963.62    8197.81   37326.12       30671.62   27656.09     23925.17
Delete             5684.04   12211.04   55330.80       56920.03    5432.65     27020.85
Geometric Mean    16971.35   17056.61   47573.13       28085.77   11493.56     45197.19
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     5917.12    6730.08    5427.61        1713.82    4161.41     12936.88
Insert: Batch      8159.04    7575.02   14621.10        8006.42    5237.04     17251.62
Insert: Bulk      34193.66   45657.46          —       39025.97          —     46119.48
Filter: Large     76850.27   41305.82  190535.30       85320.45   26649.25    227563.79
Filter: Small     28063.99   25939.28  140991.14       30955.80   30140.80     62900.97
Get                2989.02    3437.84   10282.67        2501.26    6735.42      5554.43
Filter: dict     115925.18   62251.57  100346.77       87957.53          —    286676.00
Filter: tuple    121190.93   62244.85  189147.41      325820.53          —    279165.85
Update: Whole      4310.54    5268.01   23306.60       11499.54   13548.28     19234.74
Update: Partial    4822.90    8406.46   30771.52       14645.08   27750.82     23904.07
Delete              898.24   12055.36   25639.10         560.90    3697.52     26173.26
Geometric Mean     13534.6   16011.88   38758.74       15139.48   10637.15     42360.87
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     2887.51    2706.10    3124.89        1555.69    2168.91      6933.13
Insert: Batch      3338.14    2836.43    5260.97        4935.80    2465.98      8990.28
Insert: Bulk       5953.94    7625.00          —       17844.05          —     15476.21
Filter: Large     25540.46   14900.14   51151.17       28043.62   12869.16     29844.99
Filter: Small     13449.23    9844.98   63883.50       12663.18   13649.02     21205.62
Get                1437.03    1177.15    5802.84         986.79    3691.46      2713.49
Filter: dict      32532.41   23278.43   20152.74       21838.25          —     30630.51
Filter: tuple     35202.79   24822.37   50943.52       47746.16          —     32238.24
Update: Whole      2696.80    1435.15   18327.27       13814.61   12089.34      9136.96
Update: Partial    4543.57    8307.97   23618.52       17177.39   24101.25     22246.06
Delete             4928.12   12249.64   40242.69       32736.68    3458.30     25884.08
Geometric Mean     6994.09    6484.86   18820.22        11314.2    6575.42     14993.17
=============== ========== ========== ========== ============== ========== ============


PyPy7.2-Py3.6:

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4844.65    5699.46    6069.36         928.29      4602.28
Insert: Batch      6623.80    5942.15   14888.52        6750.90     21913.57
Insert: Bulk      15833.01   19876.12          —       19456.28     35732.64
Filter: Large    145843.64   96627.96  212065.79      110034.60     82509.28
Filter: Small      4867.78   61654.60  172243.99       56155.40     37690.85
Get                3538.23    7448.17    5911.03        4175.23      7216.67
Filter: dict     142764.62  109864.27  131992.03      121185.63     86464.33
Filter: tuple    143723.62  106352.47  206592.66      263009.74    114269.08
Update: Whole      6448.56   14572.05   19806.92       23459.62     21227.50
Update: Partial    7320.68   20191.26   32069.98       40098.96     31612.84
Delete             8583.36   29682.59   73035.62       83364.88     32051.25
Geometric Mean    15281.28   25564.53   43575.11       27864.52     29917.64
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4856.53    6099.71    6302.97         886.47      4224.78
Insert: Batch      6388.57    5979.01   14255.97        4636.63     14709.41
Insert: Bulk      15675.79   18751.54          —       17444.69     37092.82
Filter: Large    130201.72   86533.17  311024.40      110243.82     67828.80
Filter: Small      3845.09   65312.52  183754.86       47955.16     35296.59
Get                3540.29    7934.10    9121.36        4233.04      5888.39
Filter: dict     138333.47  105259.77  237840.16      119919.30     66525.03
Filter: tuple    155187.72   89280.79  335520.30      260503.32     99152.44
Update: Whole      6693.48   13079.63   37170.20       18749.98     17175.61
Update: Partial    7609.05   17583.81   47285.79       27172.58     24171.52
Delete             2339.78   36752.54   41859.66         655.36     12826.34
Geometric Mean    13247.47   25048.86    55454.4       15927.71     23380.74
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     1965.02    3519.71    4207.43         670.29      3294.88
Insert: Batch      1904.72    3493.31    7636.38        4421.69      8557.21
Insert: Bulk       4054.34    7156.34          —       13786.11     17747.40
Filter: Large     20301.33   29613.15  122365.02       38721.68      2934.91
Filter: Small      1908.01   26244.67  105406.30       24031.37      2634.84
Get                2111.95    4936.50    6633.01        2315.14      1354.96
Filter: dict      28415.33   39443.07   75871.80       28089.40      3113.37
Filter: tuple     26695.73   39080.83  125314.67       58677.38     10182.81
Update: Whole      4072.91    5559.29   27090.75       11341.40      9704.97
Update: Partial    7782.08   20601.30   37512.08       14907.51     30243.79
Delete             9303.80   26078.32   59424.56       63702.66     34440.70
Geometric Mean     5855.94   12832.73   33099.23       12839.01      6897.17
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
* ``Django`` is marginally slower
* ``Tortoise ORM`` is notably slower, but notably faster for Updates & Deletes
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
* ``base.executor._field_to_db()`` could be replaced with a pre-computed dict lookup
* ``Queryset.resolve_filters`` is doing lots of unnecessary stuff, especially for .get() method
* Get operation is slow (likely slow SQL generation, could be resolved with parametrized query cacheing)


On Bulk inserts
^^^^^^^^^^^^^^^
Bulk inserts is noticeably faster if inside a transaction.
We can't safely force a transaction around the entire bulk operation, so leave it as is until we have a safe chunking operation.


On Queryset performance
^^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.

Also, we can make more queries use parameterised queries, cache SQL generation, and cache prepared queries.

It seems in cases where we can avoid using PyPika (and use prepared statements), PyPy performance increase is even larger than CPython.


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

15) **Know about default converters & native DB types** *(generic)*

    (20-25% speedup for Fetch operations) https://github.com/tortoise/tortoise-orm/pull/190
