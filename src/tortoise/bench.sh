#!/bin/sh

cd $(dirname $0)

PYPY=`python -V | grep PyPy`

# setup DB
rm -f /dev/shm/db.sqlite3

if [ -z "$PYPY" ]
then
    # run uvloop benchmarks
    PYTHONUNBUFFERED=x UVLOOP=1 python -m bench
else
    # run regular loop benchmarks
    PYTHONUNBUFFERED=x python -m bench
fi

# teardown DB
rm -f /dev/shm/db.sqlite3
