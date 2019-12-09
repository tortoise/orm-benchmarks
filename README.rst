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
Insert: Single     5925.70    6414.47    6317.45        1912.47    4105.97      9384.44
Insert: Batch      8525.78    7146.36   21325.47       10414.41    5512.25     11378.26
Insert: Bulk      32522.18   42963.86          —       37018.31          —     90154.52
Filter: Large     72874.33   42302.91  183146.18      103691.33   28379.17    243688.17
Filter: Small     28878.83   26896.43  138171.28       31611.61   30840.43     67630.68
Get                3062.78    3557.88   10029.49        2622.19    6825.52      5224.01
Filter: dict     102849.63   58590.29  105475.29       98106.79          —    344036.52
Filter: tuple    113750.32   56135.67  179878.91      303696.66          —    282713.78
Update: Whole      4364.79    6098.86   23406.04       19930.14   12842.80     13672.23
Update: Partial    5014.29    7687.03   33645.81       32165.03   25164.08     18949.32
Delete             5306.94   11428.56   48746.04       57606.81    4973.33     20286.83
Geometric Mean    15710.52   15676.26   43614.05       27561.93   11018.84      40036.8
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     5538.69    5991.89    5086.09        1604.15    3913.48      9337.70
Insert: Batch      7963.72    6781.75   13396.97        7479.96    5083.72     11367.20
Insert: Bulk      28604.68   41932.56          —       36374.47          —     76075.42
Filter: Large     70294.42   38637.55  173778.29       95911.02   28179.81    219456.13
Filter: Small     27663.99   24963.70  134822.68       30162.65   29522.70     63997.49
Get                2903.97    3285.01    9554.32        2319.34    6607.20      5099.74
Filter: dict     100416.63   55857.40   93938.33       88341.43          —    335109.57
Filter: tuple    110792.96   57737.47  168283.07      279935.66          —    273667.10
Update: Whole      4082.10    5351.75   22020.38       12029.99   12704.55     12281.27
Update: Partial    4687.65    7809.13   28488.49       16127.49   25205.51     18740.30
Delete              851.78   11427.32   24633.65        1146.62    3478.44      3435.49
Geometric Mean    12618.99   14946.37   36068.29       15872.56   10249.72     32444.92
=============== ========== ========== ========== ============== ========== ============

=============== ========== ========== ========== ============== ========== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM
=============== ========== ========== ========== ============== ========== ============
Insert: Single     2808.15    2843.01    2999.86        1508.95    2046.42      5980.88
Insert: Batch      3255.72    3103.10    4963.87        4677.45    2393.82      7476.02
Insert: Bulk       5786.89    9689.74          —       17441.02          —     18855.13
Filter: Large     24048.26   13578.53   47961.72       28415.86   13265.43     28645.53
Filter: Small     12651.70    9404.07   61953.42       11880.25   13144.76     19919.50
Get                1357.47    1115.84    5151.41         948.22    3360.56      2501.03
Filter: dict      29923.09   21194.62   19645.88       24041.81          —     37964.37
Filter: tuple     33237.23   21906.61   47153.22       43507.47          —     32612.02
Update: Whole      2548.49    1500.35   16624.50       14243.06   10295.22      8360.13
Update: Partial    4401.40    7655.23   21497.07       17689.72   22492.40     18438.59
Delete             4900.97   11207.85   37662.76       31191.72    3247.57     17201.64
Geometric Mean     6686.61    6392.17   17593.94       11127.67    6191.21     13968.31
=============== ========== ========== ========== ============== ========== ============


PyPy7.2-Py3.6:

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4844.65    5699.46    6069.36         928.29      4119.27
Insert: Batch      6623.80    5942.15   14888.52        6750.90     19889.84
Insert: Bulk      15833.01   19876.12          —       19456.28     59792.55
Filter: Large    145843.64   96627.96  212065.79      110034.60     83070.61
Filter: Small      4867.78   61654.60  172243.99       56155.40     40043.36
Get                3538.23    7448.17    5911.03        4175.23      8464.85
Filter: dict     142764.62  109864.27  131992.03      121185.63     94067.34
Filter: tuple    143723.62  106352.47  206592.66      263009.74    126491.99
Update: Whole      6448.56   14572.05   19806.92       23459.62     25520.65
Update: Partial    7320.68   20191.26   32069.98       40098.96     36326.02
Delete             8583.36   29682.59   73035.62       83364.88     37541.98
Geometric Mean    15281.28   25564.53   43575.11       27864.52     33369.34
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4856.53    6099.71    6302.97         886.47      4709.30
Insert: Batch      6388.57    5979.01   14255.97        4636.63     19616.08
Insert: Bulk      15675.79   18751.54          —       17444.69     62711.06
Filter: Large    130201.72   86533.17  311024.40      110243.82     69154.04
Filter: Small      3845.09   65312.52  183754.86       47955.16     36348.92
Get                3540.29    7934.10    9121.36        4233.04      6100.74
Filter: dict     138333.47  105259.77  237840.16      119919.30     77601.55
Filter: tuple    155187.72   89280.79  335520.30      260503.32    116994.87
Update: Whole      6693.48   13079.63   37170.20       18749.98     22658.09
Update: Partial    7609.05   17583.81   47285.79       27172.58     35797.50
Delete             2339.78   36752.54   41859.66         655.36     40024.90
Geometric Mean    13247.47   25048.86    55454.4       15927.71     31084.92
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     1965.02    3519.71    4207.43         670.29      3592.01
Insert: Batch      1904.72    3493.31    7636.38        4421.69     12099.74
Insert: Bulk       4054.34    7156.34          —       13786.11     24692.28
Filter: Large     20301.33   29613.15  122365.02       38721.68      2855.62
Filter: Small      1908.01   26244.67  105406.30       24031.37      2478.21
Get                2111.95    4936.50    6633.01        2315.14      1348.12
Filter: dict      28415.33   39443.07   75871.80       28089.40      2995.77
Filter: tuple     26695.73   39080.83  125314.67       58677.38     10422.97
Update: Whole      4072.91    5559.29   27090.75       11341.40     12903.72
Update: Partial    7782.08   20601.30   37512.08       14907.51     31801.49
Delete             9303.80   26078.32   59424.56       63702.66     42910.38
Geometric Mean     5855.94   12832.73   33099.23       12839.01      7698.50
=============== ========== ========== ========== ============== ============

Results (PostgreSQL)
====================

PostgreSQL 11.4 on my notebook.

=============== ========== ========== ========== ============== ========== ============ ================
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     4857.31    3173.70    4146.48        1973.41    3860.16      4281.72          8468.56
Insert: Batch      4723.08    3204.96    8367.68        5521.35    4082.23     11569.12         19627.20
Insert: Bulk      21567.71   26393.30          —       11818.74          —     22509.96         51807.75
Filter: Large    166978.68  108860.91  272674.79      101980.56   60266.99    278991.61        270785.15
Filter: Small     30326.04   36784.37  148737.30       25072.68   41468.97     34928.77         62893.37
Get                2635.83    2919.64    6983.48        1975.18    6531.92      2198.19          3340.53
Filter: dict     396663.25  211728.38  115983.06       99886.58          —    521024.00        477450.14
Filter: tuple    589188.32  214534.54  278726.48      334246.11          —    421258.66        378978.83
Update: Whole      2625.43    3513.49    7965.35        8263.97    5126.85     11895.91         22601.77
Update: Partial    3074.43    4476.93    9719.73       11930.46    9258.71     13612.81         24913.88
Delete             3832.58    7484.91   13703.93       15862.13    4895.59     18205.01         28255.30
Geometric Mean    17520.28   15931.85   28364.15       16985.78    9377.11     29630.17         44662.14
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     4157.89    3221.06    3506.17        1665.17    3691.07      4221.30          8494.10
Insert: Batch      4283.49    3255.67    6645.80        4614.84    3926.67     11197.13         19173.39
Insert: Bulk      19246.64   25736.82          —       11419.44          —     21134.52         48475.89
Filter: Large    162473.05   86857.86  250163.89       98439.47   58256.31    264857.97        239937.30
Filter: Small     27572.16   32939.94  148881.53       22508.76   40001.43     33498.98         60798.78
Get                2567.59    2716.21    7079.23        1844.78    6300.94      2109.81          3252.21
Filter: dict     385401.97  184939.34  115163.91       95599.00          —    489628.43        461836.20
Filter: tuple    560058.22  183095.68  254393.35      303911.95          —    391634.77        369900.70
Update: Whole      2516.89    3247.27    7702.60        6388.40    5163.34     12362.83         20421.12
Update: Partial    2854.95    4657.43    9425.80        8548.84   10846.97     13049.14         23544.60
Delete              665.46    6858.47    7896.74         588.09    1760.15      2958.13          7263.20
Geometric Mean    14006.23   14782.69   25197.98       11160.85    8226.66     24257.46         37774.49
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     1794.81    1853.92    1711.36        1432.11    1741.26      3078.97          6219.87
Insert: Batch      1857.74    1711.45    2395.07        2258.69    1704.36      6518.37         10841.76
Insert: Bulk       3674.97    6645.29          —        5923.12          —      9747.32         19599.32
Filter: Large     35687.76   19888.51   55475.17       33835.86   19270.01     43282.34         40803.37
Filter: Small     14545.37   10525.28   62945.91       10273.93   15708.61     17877.42         26991.63
Get                1310.19     987.25    3745.50         773.24    2764.56      1488.62          2257.41
Filter: dict      46460.31   35310.28   20540.86       28408.81          —     80742.58         60991.48
Filter: tuple     55428.75   39641.53   55075.65       52119.29          —     64897.17         50287.22
Update: Whole      1590.55    1075.92    6071.77        6232.19    4900.99      7921.16         12783.71
Update: Partial    2419.78    4334.06    7705.05        8532.21    9909.75     12371.76         17175.33
Delete             3594.38    7391.54   12406.49       12780.38    3163.39     17984.49         28752.11
Geometric Mean     5891.64    5709.64    11341.1        7640.77    4985.36     13177.81          17983.5
=============== ========== ========== ========== ============== ========== ============ ================


Results (MySQL)
===============

MariaDB 10.2 on my notebook.

=============== ========== ========== ========== ============== ========== ============ ================
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     3320.40    2537.10    2083.20        1508.08    1067.54      1730.46          8390.39
Insert: Batch      4895.10    4076.56    8721.07        6322.07    3577.43      6237.53         10709.90
Insert: Bulk      23177.18   26654.36          —       23306.61          —     40720.61         48005.68
Filter: Large     95959.99   47565.21  267621.03       83575.68   52217.30     58012.53         59877.23
Filter: Small     25485.05   20762.95  146249.86       23513.51   38553.39     24959.80         32793.57
Get                2314.70    2012.00    7513.62        1945.90    5704.71      2570.90          3408.79
Filter: dict     157923.23   59769.36  126040.24       49245.40          —     64828.31         66342.41
Filter: tuple    182212.37   61706.79  270536.55      121947.35          —     60139.20         62937.60
Update: Whole      2595.80    3266.07    7740.11        7018.32    5740.50      7184.85         11953.66
Update: Partial    3262.05    4294.02   11086.85       13373.71   11806.02      9358.91         14321.83
Delete             3672.86    5276.23   14216.45       16655.89    1960.60     10409.73         15733.42
Geometric Mean    13074.49   10372.31   27207.26       14890.09    7009.52     14124.91         20855.97
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     1586.27    2324.10    2436.70        1368.95    2271.97      2322.08          7838.03
Insert: Batch      4832.89    3684.92    2800.08        4532.90    3586.95      7254.76         10704.82
Insert: Bulk      19515.33   24021.88          —       17055.18          —     37142.22         41878.97
Filter: Large     91413.79   41820.47  236439.02       77769.15   48538.18     55431.62         55681.44
Filter: Small     24398.11   18376.39  145356.40       21886.76   36773.46     23799.13         30573.80
Get                2151.93    1794.15    7206.15        1768.73    5175.08      2420.48          3051.39
Filter: dict     146894.62   56842.99  109748.40       74563.06          —     62006.11         63796.95
Filter: tuple    178222.79   55594.02  238035.47      162434.98          —     57263.45         60361.86
Update: Whole      2390.28    2654.44    7183.37        5667.65    5403.90      6509.68         11590.66
Update: Partial    2918.11    3843.06   10536.94        8958.42   10695.01      8892.55         14128.76
Delete              635.83    4281.21    8343.89         976.27    1235.34      9362.14         15272.77
Geometric Mean     9836.03    9182.79   22106.91       10607.35    6938.93     13934.08         19724.36
=============== ========== ========== ========== ============== ========== ============ ================

=============== ========== ========== ========== ============== ========== ============ ================
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Tortoise ORM C10
=============== ========== ========== ========== ============== ========== ============ ================
Insert: Single     1435.69    1419.86    1730.63        1227.01    1347.14      1539.69          5270.07
Insert: Batch      1977.81    1981.26    3121.53        2671.33    1763.92      4142.43          6096.78
Insert: Bulk       3876.03    6380.51          —        8791.78          —     10865.05         13365.76
Filter: Large     32491.41   11632.05   55128.26       27437.18   17751.39     16065.10         16129.87
Filter: Small     12689.13    5674.93   64132.62        9596.97   15649.37      9279.57         10057.63
Get                1146.18     618.04    3809.39         758.59    2792.15      1026.46          1171.64
Filter: dict      42434.09   15586.66   20486.27       23282.14          —     19189.50         19387.42
Filter: tuple     49092.71   14679.77   54900.20       39348.18          —     17527.12         17657.66
Update: Whole      1585.46    1035.29    6552.43        6025.16    4927.34      3260.95          6674.50
Update: Partial    2638.86    4161.22    9415.52        8849.84   12124.56      8939.23         13617.46
Delete             3394.26    5498.52   12334.46       12709.96     806.88      9490.54         15447.82
Geometric Mean      5549.9    3979.97   12006.83        7386.97    4155.09      6571.33          9184.61
=============== ========== ========== ========== ============== ========== ============ ================


Quick analysis
--------------
* Pony ORM is heavily optimised for performance.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is competitive.
* ``Get`` is surprisingly slow for everyone.
* Pony ORM, SQLAlchemy & SQLObject does merge operations for updates, so is technically always partial updates.
* Tortoise ORM performance using the ``asyncpg`` PostgreSQL driver is really good, winning overall.
* Tortoise ORM performance using the ``aiomysql`` MySQL driver is mediocre, the driver itself is taking the majority of CPU time.

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

16) **Connection Pooling** *(MySQL & PostgreSQL)*

    (30-50% speedup overall) https://github.com/tortoise/tortoise-orm/pull/229

17) **Many small tweaks** *(generic)*

    (5-30% depending on driver) https://github.com/tortoise/tortoise-orm/pull/241
