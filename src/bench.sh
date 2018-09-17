#!/bin/sh

export ITERATIONS=100
if [ "x$1" == "xfull" ]; then
    export ITERATIONS=100000
fi

echo Iterations: $ITERATIONS

printf '' > outfile

django/bench.sh | tee -a outfile
peewee/bench.sh | tee -a outfile
pony/bench.sh | tee -a outfile
#sqlalchemy/bench.sh
#sqlobject/bench.sh
#tortoise/bench.sh

cat outfile | ./present.py

rm -f outfile
