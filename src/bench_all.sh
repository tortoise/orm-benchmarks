#!/bin/sh

echo > results

DBTYPE=sqlite ./bench.sh $1
DBTYPE=postgres ./bench.sh $1
DBTYPE=mysql ./bench.sh $1

cat results
