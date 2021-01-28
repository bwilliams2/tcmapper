FROM postgis/postgis:13-3.1-alpine
COPY dump_26-01-2021_11_23_25.gz /tmp/sql_backup.sql.gz
COPY restore_database.sh /docker-entrypoint-initdb.d/
EXPOSE 5432
