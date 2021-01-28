#! /bin/bash
psql -U postgres -h localhost -Atc "select tablename from pg_tables where schemaname='public'" postgres |\
  while read TABLENAME; do
        echo "$TABLENAME"
    psql -U postgres -h localhost -c "COPY $TABLENAME TO STDOUT WITH CSV HEADER" postgres | gzip -c > ./csvs/$TABLENAME.csv.gz
  done