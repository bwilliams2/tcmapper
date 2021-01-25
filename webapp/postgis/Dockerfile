FROM postgis/postgis:13-3.1-alpine
COPY dump_24-01-21_19_36_35.gz /tmp/sql_backup.sql.gz
COPY restore_database.sh /docker-entrypoint-initdb.d/
EXPOSE 5432
