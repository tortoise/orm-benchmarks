#!/bin/sh

# setup DB
if [ "$DBTYPE" = "postgres" ]
then
    psql -U postgres -w -c 'drop database tbench';
    psql -U postgres -w -c 'create database tbench';
elif [ "$DBTYPE" = "mysql" ]
then
    echo 'DROP DATABASE tbench' | mysql -u root
    echo 'CREATE DATABASE tbench' | mysql -u root
else
    rm -f /dev/shm/db.sqlite3
fi
