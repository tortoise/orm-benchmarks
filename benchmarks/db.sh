#!/bin/sh

export PATH="/opt/homebrew/opt/libpq/bin:$PATH"

# setup DB
if [ "$DBTYPE" = "postgres" ]
then
    PGPASSWORD=$PASSWORD psql -h 127.0.0.1 -p ${PGPORT:-5432} -U postgres -w -c 'drop database if exists tbench';
    PGPASSWORD=$PASSWORD psql -h 127.0.0.1 -p ${PGPORT:-5432} -U postgres -w -c 'create database tbench';
elif [ "$DBTYPE" = "mysql" ]
then
    docker exec -i bench-mysql mysql -u root -p$PASSWORD -e 'DROP DATABASE IF EXISTS tbench; CREATE DATABASE tbench;' 2>/dev/null
else
    rm -f /tmp/db.sqlite3
fi
