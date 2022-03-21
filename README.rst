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

Py39:

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     1497.95    4872.62    1644.55         976.67    1420.88      5347.90    5347.90 Tortoise ORM
Insert: Batch      4479.47    6113.61   17873.20        8009.59    4134.64      6585.81   17873.20   Pony ORM
Insert: Bulk      16263.30   19282.38          —       17151.81          —     22266.31   22266.31 Tortoise ORM
Filter: Large     72808.51   37053.46  113551.38       77921.94   30458.51     31078.13  113551.38   Pony ORM
Filter: Small     27091.89   21447.86   14085.46       26718.01   28338.93     18595.55   28338.93  SQLObject
Get                3297.72    3342.47    7482.68        3335.06    6650.92      3286.47    7482.68   Pony ORM
Filter: dict      98377.01   42442.45   91354.29       72774.82          —     37338.13   98377.01     Django
Filter: tuple    104145.07   44562.58  111963.06      120148.50          —     35421.57  120148.50 SQLAlchemy ORM
Update: Whole      4390.65    5908.89   23083.68       16193.39   12167.63      8778.30   23083.68   Pony ORM
Update: Partial    4799.47    7789.01   31692.20       29134.53   23880.80     10027.27   31692.20   Pony ORM
Delete             4923.51   10720.91   47743.93       46426.27    1602.24     10481.33   47743.93   Pony ORM
Geometric Mean    12016.85   12731.01   25699.52       19750.85    7934.03     13016.58   30488.23   Pony ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     1375.24    4739.11    1560.53         826.58    1360.56      5235.68    5235.68 Tortoise ORM
Insert: Batch      4214.45    6076.06   13350.85        2710.25    4431.66      6643.60   13350.85   Pony ORM
Insert: Bulk      14587.36   18580.24          —        9334.37          —     20513.05   20513.05 Tortoise ORM
Filter: Large     70246.54   34803.17  107677.40       68477.31   29510.34     29973.02  107677.40   Pony ORM
Filter: Small     25822.56   18710.87   14796.78       21498.59   26458.48     18192.33   26458.48  SQLObject
Get                3061.19    3254.31    8124.48        2930.53    6272.33      3238.39    8124.48   Pony ORM
Filter: dict      92273.77   45158.31   82152.66       63156.77          —     37411.62   92273.77     Django
Filter: tuple     92140.65   43432.18  107504.91      104278.85          —     34485.92  107504.91   Pony ORM
Update: Whole      4041.05    5293.05   22296.49       12227.82   11964.75      8385.37   22296.49   Pony ORM
Update: Partial    4718.18    7761.19   32753.93       18142.24   23089.39      8583.97   32753.93   Pony ORM
Delete              949.35   10826.34   15739.36        1126.62    1258.04      7853.74   15739.36   Pony ORM
Geometric Mean     9708.83    12316.1   22066.86       10365.98    7523.29     12234.09    26072.4   Pony ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     1158.99    2579.05    1341.74         795.49    1010.96      3012.69    3012.69 Tortoise ORM
Insert: Batch      2565.09    2814.82    5110.64        5135.04    2652.73      3816.79    5135.04 SQLAlchemy ORM
Insert: Bulk       3899.39    7228.57          —       11383.03          —      7544.93   11383.03 SQLAlchemy ORM
Filter: Large     23726.12   12886.49   45353.88       32007.81   16424.68     13818.28   45353.88   Pony ORM
Filter: Small     12567.48    7681.68    4872.43       16312.17   15380.60     10183.42   16312.17 SQLAlchemy ORM
Get                1780.10    1121.88    5418.16        2838.25    3760.11      2064.30    5418.16   Pony ORM
Filter: dict      30270.60   18113.41   23406.96       26928.97          —     15463.37   30270.60     Django
Filter: tuple     32982.30   18634.59   45589.27       39613.25          —     14293.40   45589.27   Pony ORM
Update: Whole      2520.12    1460.37   16595.00       13253.82   10368.59      4979.73   16595.00   Pony ORM
Update: Partial    4281.07    7621.57   21649.70       21192.27   22376.78      8353.98   22376.78  SQLObject
Delete             4725.69   10672.44   39093.15       38714.27    1436.19      8972.24   39093.15   Pony ORM
Geometric Mean     5920.37    5764.76   12853.14       12079.92    5509.39       7032.0   15685.54   Pony ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========



PyPy7.3-Py3.6: (Outdated)

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4092.94    6042.45    6166.89        1004.98      6786.58
Insert: Batch      4529.93    6456.81   18247.22        6982.63     26348.64
Insert: Bulk      17961.11   24302.27          —       21428.22     80531.38
Filter: Large    152801.52   91886.54  295678.67      129700.40     90993.88
Filter: Small      6099.36   65094.77  175134.68       60966.19     45463.05
Get                4255.07    6793.41    8310.16        4339.15      9229.52
Filter: dict     147533.08  116293.38  215108.01      109211.59     94985.63
Filter: tuple    175529.83  122951.45  281181.48      253415.27    130914.54
Update: Whole      6710.01   16514.91   41939.12       22677.70     30434.61
Update: Partial    8089.69   23377.04   51308.13       43023.59     38576.48
Delete             8766.41   29169.88   74799.44       81948.65     42805.28
Geometric Mean    15887.12   27270.66   58524.96       28825.51     39281.41
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     4089.62    5982.16    5927.49         818.31      8128.96
Insert: Batch      4582.76    6909.47   15558.25        6012.19     25381.23
Insert: Bulk      16201.10   24021.67          —       20294.09     77993.66
Filter: Large    138968.39   90818.94  279382.51      118860.29     71640.16
Filter: Small      5439.62   62951.57  168192.03       52251.13     38208.34
Get                4092.11    6989.34    8230.02        3379.57      8430.82
Filter: dict     134900.00  112626.68  202932.98       94477.51     71689.52
Filter: tuple    159685.66  122797.29  274293.13      223882.76    119104.10
Update: Whole      6201.26   11396.24   35644.86       17562.70     28303.72
Update: Partial    7669.88   23086.17   41247.77       25492.40     35430.58
Delete             2087.76   34330.64   38098.81         633.66       369.97
Geometric Mean    13135.78   26719.72   50653.72       15519.07     23445.05
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2194.07    3827.50    4030.12         792.54      5429.88
Insert: Batch      2072.86    3928.59    7509.87        4841.25     15489.04
Insert: Bulk       4747.82    9996.01          —       15407.30     29085.53
Filter: Large     25016.73   30627.76  122459.86       37727.96      2968.21
Filter: Small      1508.74   24123.13   98162.15       21523.32      2454.28
Get                2231.56    4443.86    6313.33        2312.70      1490.23
Filter: dict      29467.52   40064.73   81433.44       27085.70      3001.12
Filter: tuple     31329.65   46774.06  123617.06       45894.78      8845.51
Update: Whole      4220.60    6984.34   29109.60       10686.28     11302.96
Update: Partial    7346.76   21125.93   33835.74       14716.48     24182.52
Delete             9083.28   31221.47   64601.85       64029.41     41709.27
Geometric Mean     6146.34   14064.74   32867.64       12702.84      7951.76
=============== ========== ========== ========== ============== ============


Results (PostgreSQL)
====================

PostgreSQL 14.2 on my iMac.

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     2697.46    2350.95    1438.77        1528.94    2391.13      2127.20    2697.46     Django
Insert: Batch      3275.14    2845.78    4710.80        4742.43    2911.46     10351.19   10351.19 Tortoise ORM
Insert: Bulk      10283.94   12309.04          —        8018.63          —      6395.90   12309.04     peewee
Filter: Large     82726.80   63288.60  131699.63       58844.30   50097.69     60394.02  131699.63   Pony ORM
Filter: Small     21555.97   21030.33   15793.05       20046.59   38191.14     27055.55   38191.14  SQLObject
Get                2407.95    2351.78    4403.82        2303.46    5057.52      3289.33    5057.52  SQLObject
Filter: dict      98132.27   84224.66  102139.41       60221.74          —     84444.54  102139.41   Pony ORM
Filter: tuple    106625.81   85903.08  136295.97       88605.19          —     80993.53  136295.97   Pony ORM
Update: Whole      2921.10    2971.09    4567.47        6585.60    3444.53     15486.60   15486.60 Tortoise ORM
Update: Partial    2797.47    4698.24    8153.30        9595.10    7100.51     18292.88   18292.88 Tortoise ORM
Delete             3068.43    4037.09   10634.38        9627.40    3026.73     20908.43   20908.43 Tortoise ORM
Geometric Mean    10021.18   10045.33   14237.59        11602.3    6874.29     16828.99   22424.22 Tortoise ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     2539.09    2328.50    1411.27        1224.83    2251.15      6191.22    6191.22 Tortoise ORM
Insert: Batch      3047.01    2868.06    4822.54        4451.61    2329.81     11730.02   11730.02 Tortoise ORM
Insert: Bulk      10221.78   13097.38          —        5323.13          —     24089.97   24089.97 Tortoise ORM
Filter: Large     76022.33   56985.76  129987.42       55025.55   48907.18     66584.00  129987.42   Pony ORM
Filter: Small     25138.05   23036.83   13473.45       15691.13   35394.67     29498.84   35394.67  SQLObject
Get                2369.76    2428.95    6715.08        2186.10    4299.78      3345.98    6715.08   Pony ORM
Filter: dict      89768.94   77124.33   94526.98       52507.12          —     84390.74   94526.98   Pony ORM
Filter: tuple     93446.95   76994.08  133410.86       76779.38          —     76248.52  133410.86   Pony ORM
Update: Whole      2624.86    3177.50    6538.28        4518.49    4239.80     13470.83   13470.83 Tortoise ORM
Update: Partial    2755.20    4391.80    7717.85        6744.77    8232.20     17027.82   17027.82 Tortoise ORM
Delete              705.78    6002.87    6820.62         780.78    1502.48     18380.23   18380.23 Tortoise ORM
Geometric Mean     8432.77   10302.12   14258.86        7650.52    6150.27     20779.73    25428.1 Tortoise ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     1659.56    1337.22    1072.47        1197.89    1362.25      2057.49    2057.49 Tortoise ORM
Insert: Batch      1926.09    1720.19    2476.65        3928.80    1634.21      5382.42    5382.42 Tortoise ORM
Insert: Bulk       4083.48    4813.74          —        5169.09          —      8218.97    8218.97 Tortoise ORM
Filter: Large     29212.11   15313.77   46597.16       28275.76   23833.91     25190.86   46597.16   Pony ORM
Filter: Small     11936.52    7643.78    6958.63       10994.92   19048.65     14186.21   19048.65  SQLObject
Get                1481.25     905.49    3998.63        1917.48    3190.46      2247.54    3998.63   Pony ORM
Filter: dict      30291.07   22944.69   24043.02       24225.81          —     28221.54   30291.07     Django
Filter: tuple     37316.20   24910.94   48191.83       35775.67          —     27661.74   48191.83   Pony ORM
Update: Whole      1660.00    1141.62    5982.29        4790.04    4137.46      7815.69    7815.69 Tortoise ORM
Update: Partial    2902.67    4413.85    6453.72        7099.40    8381.57     17360.03   17360.03 Tortoise ORM
Delete             3392.16    6421.26   10231.13        8968.32    2034.67     19775.12   19775.12 Tortoise ORM
Geometric Mean      5444.3    4644.73    8313.06        7434.18    4673.36     10394.95   12595.03 Tortoise ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========


Results (MySQL)
===============

MySQL 8.0.28 on my iMac.

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     1209.92    1001.09    1053.19        1347.27    1908.04      6876.58    6876.58 Tortoise ORM
Insert: Batch       749.83    2558.92    3963.25        1530.72    2953.42      9431.34    9431.34 Tortoise ORM
Insert: Bulk       3987.40   12345.27          —       10112.36          —     22422.24   22422.24 Tortoise ORM
Filter: Large     49227.96   57264.03   87150.75       58957.62   46543.39     48015.57   87150.75   Pony ORM
Filter: Small     14872.76   16482.54    4844.00       16099.81   33623.56     27429.86   33623.56  SQLObject
Get                1955.32    2397.74    4140.78        2462.82    4124.88      3611.48    4140.78   Pony ORM
Filter: dict      56656.05   70404.15   60058.48       51717.04          —     56083.08   70404.15     peewee
Filter: tuple     55412.78   71583.70   86158.07       76517.45          —     52624.17   86158.07   Pony ORM
Update: Whole      2166.47    1924.82    4370.82        6054.75    3347.90     11290.19   11290.19 Tortoise ORM
Update: Partial    2699.93    4266.03    7172.51       10429.35    8004.78     13482.17   13482.17 Tortoise ORM
Delete             2852.52    4261.78    7971.99       11119.38    1466.69     15008.68   15008.68 Tortoise ORM
Geometric Mean     5843.52    8284.89    9942.11       10279.79    5880.45     17482.86   20324.93 Tortoise ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     1635.09    1211.99    1503.17        1193.35    1833.09      6608.95    6608.95 Tortoise ORM
Insert: Batch      2169.06    3424.20    3730.49        3134.71    2808.82      9012.26    9012.26 Tortoise ORM
Insert: Bulk       5156.00   12022.20          —        6509.26          —     19639.93   19639.93 Tortoise ORM
Filter: Large     47022.58   50669.92   90269.00       53166.04   42782.43     46612.01   90269.00   Pony ORM
Filter: Small     13620.37   19250.93    7432.71       15309.16   32922.06     26025.83   32922.06  SQLObject
Get                1810.18    1743.56    5457.96        2251.67    5029.05      3303.88    5457.96   Pony ORM
Filter: dict      52659.40   64137.99   71828.88       50016.54          —     49126.48   71828.88   Pony ORM
Filter: tuple     52679.69   65446.35   90069.34       72336.37          —     50094.20   90069.34   Pony ORM
Update: Whole      2347.67    1706.10    5001.29        5288.58    3714.30     10855.70   10855.70 Tortoise ORM
Update: Partial    2446.26    4068.74    6731.51        8148.18    7689.34     13793.14   13793.14 Tortoise ORM
Delete              611.18    5633.39    5323.53         805.95    1113.54     15653.61   15653.61 Tortoise ORM
Geometric Mean     5700.18    8359.38   10906.27        7695.76    5728.65     16637.86   20627.76 Tortoise ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========

=============== ========== ========== ========== ============== ========== ============ ========== ==========
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM SQLObject  Tortoise ORM Max        Best ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========
Insert: Single     1161.88    1197.36     868.83        1080.28    1200.52      3517.80    3517.80 Tortoise ORM
Insert: Batch      1136.71    1782.50    2086.51        2289.90    1775.70      4093.84    4093.84 Tortoise ORM
Insert: Bulk       2947.01    4774.88          —        5026.13          —      6676.91    6676.91 Tortoise ORM
Filter: Large     21409.92   15339.61   42885.45       26865.84   22947.41     17383.94   42885.45   Pony ORM
Filter: Small      7377.32    7753.80    5326.22       11604.61   18188.73      9937.04   18188.73  SQLObject
Get                 912.97     897.40    3436.21        1932.07    2808.04      1647.64    3436.21   Pony ORM
Filter: dict      23786.67   18481.91   20365.59       23747.48          —     17939.35   23786.67     Django
Filter: tuple     29319.45    9438.12   42158.68       33278.53          —     16991.10   42158.68   Pony ORM
Update: Whole      1572.93    1061.51    3674.52        5221.10    3289.43      3302.92    5221.10 SQLAlchemy ORM
Update: Partial    2348.49    3900.11    5711.35        7318.67    7214.52      4440.85    7318.67 SQLAlchemy ORM
Delete             2464.61    5020.07    6816.90        9002.52    1637.52      6402.34    9002.52 SQLAlchemy ORM
Geometric Mean     3941.19    3977.64    6671.87        7018.64    4201.45      6434.92     9893.7 SQLAlchemy ORM
=============== ========== ========== ========== ============== ========== ============ ========== ==========




PyPy7.3-Py3.6: (Outdated)

=============== ========== ========== ========== ============== ============
Test 1          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2479.55    2663.10    3088.68         686.92      3311.91
Insert: Batch      3478.12    4571.76    5194.87        4214.03     13584.52
Insert: Bulk      14553.90   19480.48          —       15260.41     55214.98
Filter: Large     80983.35  175029.85  479457.80       59215.04    160185.46
Filter: Small      4995.72   37628.16  136060.23       18990.66     24888.53
Get                2868.25    4870.54    6107.97        2630.39      6538.67
Filter: dict      80650.88  219339.95  301358.89       52242.19    183104.50
Filter: tuple     93584.59  257332.26  490594.29       74740.17    175407.06
Update: Whole      3563.43    7760.36    5348.80        5540.23     11161.77
Update: Partial    4536.02   10036.94   11210.07       12264.97     14984.03
Delete             4978.72   10073.98   11107.52       10907.25     12449.24
Geometric Mean     9889.22   20926.09   30192.66       11285.31     26393.92
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 2          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     2266.32    2663.82    2669.34         597.25      3513.88
Insert: Batch      3328.18    4435.96    6949.97        3773.89     10493.08
Insert: Bulk      14065.42   18684.71          —       14458.93     55861.34
Filter: Large     80296.63  164763.64  447302.97       54498.39    153077.80
Filter: Small      4800.15   35434.65  130211.62       17627.65     21258.96
Get                2565.44    4543.19    5849.48        2310.20      6251.27
Filter: dict      77842.51  207108.12  280970.71       50958.86    185933.49
Filter: tuple     91267.58  239574.53  438762.04       73630.97    172285.95
Update: Whole      2701.75    5406.82    6975.43        4327.97      9913.26
Update: Partial    4539.54    9879.36   10746.90       10125.79     14495.50
Delete             1176.44    7017.19    6249.98        1387.88      8181.26
Geometric Mean     8165.06   18884.27   28591.56        8489.41     24079.39
=============== ========== ========== ========== ============== ============

=============== ========== ========== ========== ============== ============
Test 3          Django     peewee     Pony ORM   SQLAlchemy ORM Tortoise ORM
=============== ========== ========== ========== ============== ============
Insert: Single     1008.08    1582.11    1617.94         465.03      2258.82
Insert: Batch      1492.21    2833.39    3595.88        2126.38      6739.82
Insert: Bulk       3357.71    6484.93          —        6410.32     16790.12
Filter: Large     12164.83   40576.68  109275.41        9531.62     34746.82
Filter: Small      2314.81   12551.29   58031.65        5503.53      9873.51
Get                1083.01    2165.71    2800.69         854.14      2358.51
Filter: dict      12742.82   54209.15   73098.84        8640.37     46526.40
Filter: tuple     13728.33   62009.01  107794.63       10255.39     42013.15
Update: Whole      1589.21    2352.14    4388.50        3946.67      5021.95
Update: Partial    3894.78    8822.50    6142.39        7243.80     14487.33
Delete             3791.23    8238.25    8413.57        8394.18     11540.60
Geometric Mean      3367.9    8574.74   13385.55         4134.8     11175.14
=============== ========== ========== ========== ============== ============


Quick analysis
--------------
* Pony ORM is heavily optimised for performance.
* Django & SQLAlchemy is surprisingly similar in performance.
* Tortoise ORM is competitive.
* ``Get`` is surprisingly slow for everyone.
* Pony ORM, SQLAlchemy & SQLObject does merge operations for updates, so is technically always partial updates.
* Tortoise ORM performance using the ``asyncpg`` PostgreSQL driver is really good, winning overall.
* Tortoise ORM performance using the ``aiomysql`` MySQL driver is mediocre, the driver itself is taking the majority of CPU time. PyPy runs this driver a lot faster, which indicates that the slow paths are likely just in Python itself.

PyPy comparison: SQLite
-----------------------
* ``peewee`` and ``Pony ORM`` gets a noticeable performance improvement
* ``SQLAlchemy ORM`` and ``Django`` performs similarily
* ``Tortoise ORM`` has slow Reads and fast Create, Update & Delete operation
* ``SQLObject`` fails

PyPy comparison: MySQL
-----------------------
* ``peewee`` and ``Tortoise ORM`` gets a noticeable performance improvement
* ``Pony ORM`` is marginally faster
* ``SQLAlchemy ORM`` and ``Django`` is marginally slower
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


On Queryset performance
^^^^^^^^^^^^^^^^^^^^^^^
Since pypika is immutable, and our Queryset object is as well, we need tests to guarantee our immutability.
Then we can aggresively cache querysets.

Also, we can make more queries use parameterised queries, cache SQL generation, and cache prepared queries.

It seems in cases where we can cache the PyPika result (and use prepared statements), PyPy performance increase is even larger than CPython.


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
