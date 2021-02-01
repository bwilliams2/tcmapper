FROM postgis/postgis:13-3.1-alpine
COPY dump_28-01-2021_20_47_09.gz /tmp/sql_backup.sql.gz
COPY restore_database.sh /docker-entrypoint-initdb.d/
EXPOSE 5432
