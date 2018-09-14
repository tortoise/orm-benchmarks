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
SQLAlchemy ORM:
        http://www.sqlalchemy.org/
SQLObject:
        https://github.com/sqlobject/sqlobject
Tortoise ORM:
        https://github.com/tortoise/tortoise-orm

Results
=======

==================== ============ ============ ============
\                     Django       peewee       pony
==================== ============ ============ ============
Insert                   1172.37      1275.20      1337.22
Insert: atomic           8832.62      7176.03     25803.69
Insert: bulk            31472.56     16709.06
Filter: match           73838.19     42852.70    232588.67
Filter: contains        74056.71     41891.36    221371.11
==================== ============ ============ ============
