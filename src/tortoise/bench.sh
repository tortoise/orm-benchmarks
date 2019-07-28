#!/bin/sh

cd $(dirname $0)

PYPY=`python -V | grep PyPy`

# setup DB
rm -f /dev/shm/db.sqlite3
# run regular loop benchmarks
PYTHONUNBUFFERED=x python -m bench

if [ -z "$PYPY" ]
then
    # setup DB
    rm -f /dev/shm/db.sqlite3
    # run uvloop benchmarks
    PYTHONUNBUFFERED=x UVLOOP=1 python -m bench
fi

# teardown DB
rm -f /dev/shm/db.sqlite3
