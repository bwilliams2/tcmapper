gunzip -c ./dump_28-01-2021_20_47_09.sql.gz > /tmp/db_backup.sql
export PGPASSWORD=$RDS_PASSWORD
# psql -U $RDS_USER -h $RDS_HOST -c "CREATE DATABASE postgres_django"
psql \
   -f /tmp/db_backup.sql \
   --host $RDS_HOST \
   --port $RDS_PORT \
   --username $RDS_USER \
   --dbname $RDS_DB