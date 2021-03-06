#! /bin/bash
psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS postgres_django"
psql -U postgres -h localhost -c "CREATE DATABASE postgres_django"
docker-compose -f ../../docker-compose.prod.yml exec db pg_dumpall -U postgres -h localhost | gzip -c > dump_`date +%d-%m-%Y_%H_%M_%S`.sql.gz