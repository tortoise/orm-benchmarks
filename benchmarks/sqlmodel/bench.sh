#!/bin/sh

cd $(dirname $0)

PYPY=`python -V | grep PyPy`

# setup DB
../db.sh

if [ -z "$PYPY" ]
then
    PYTHONUNBUFFERED=x UVLOOP=1 python -m bench
else
    PYTHONUNBUFFERED=x python -m bench
fi
