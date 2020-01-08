#!/bin/sh

echo > results

DBTYPE=sqlite ./bench.sh $1
python -V | grep PyPy || DBTYPE=postgres ./bench.sh $1
DBTYPE=mysql ./bench.sh $1

cat results
