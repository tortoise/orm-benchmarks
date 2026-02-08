#!/bin/sh

cd $(dirname $0)

if [ "$DBTYPE" = "mysql" ]; then
    echo "Piccolo does not support MySQL, skipping"
    exit 0
fi

PYPY=`python -V | grep PyPy`

# setup DB
../db.sh

if [ -z "$PYPY" ]
then
    PYTHONUNBUFFERED=x UVLOOP=1 python -m bench
else
    PYTHONUNBUFFERED=x python -m bench
fi
