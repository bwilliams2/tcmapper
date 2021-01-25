#! /bin/bash
psql -U postgres -c "DROP DATABASE IF EXISTS postgres_django"
psql -U postgres -c "CREATE DATABASE postgres_django"
pg_dumpall -U postgres | gzip -c > dump_`date +%d-%m-%Y_%H_%M_%S`.gz