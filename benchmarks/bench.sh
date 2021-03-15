#!/bin/sh

export ITERATIONS=100
if [ "x$1" == "xfull" ]; then
    export ITERATIONS=1000
fi
if [ "x$1" == "xextra" ]; then
    export ITERATIONS=10000
fi

cd $(dirname $0)

echo Iterations: $ITERATIONS


echo Test 1
export TEST=1
printf '' > outfile1

django/bench.sh | tee -a outfile1
peewee/bench.sh | tee -a outfile1
pony/bench.sh | tee -a outfile1
sqlalchemy/bench.sh | tee -a outfile1
sqlobject/bench.sh | tee -a outfile1
tortoise/bench.sh | tee -a outfile1


echo Test 2
export TEST=2
printf '' > outfile2

django/bench.sh | tee -a outfile2
peewee/bench.sh | tee -a outfile2
pony/bench.sh | tee -a outfile2
sqlalchemy/bench.sh | tee -a outfile2
sqlobject/bench.sh | tee -a outfile2
tortoise/bench.sh | tee -a outfile2


echo Test 3
export TEST=3
printf '' > outfile3

django/bench.sh | tee -a outfile3
peewee/bench.sh | tee -a outfile3
pony/bench.sh | tee -a outfile3
sqlalchemy/bench.sh | tee -a outfile3
sqlobject/bench.sh | tee -a outfile3
tortoise/bench.sh | tee -a outfile3

echo `python -V`, Iterations: $ITERATIONS DBtype: $DBTYPE | tee -a results
cat outfile1 | ./present.py "Test 1" | tee -a results
cat outfile2 | ./present.py "Test 2" | tee -a results
cat outfile3 | ./present.py "Test 3" | tee -a results
echo | tee -a results
