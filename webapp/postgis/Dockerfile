FROM postgis/postgis:13-3.1-alpine AS DB
COPY dump_20-01-2021_22_12_48.gz /tmp/sql_backup.sql.gz
COPY restore_database.sh /docker-entrypoint-initdb.d/
EXPOSE 5432
