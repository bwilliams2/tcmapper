
#!/usr/bin/env bash
echo "Restoring database"
# psql -U postgres -c "CREATE DATABASE commutedb"
gunzip < /tmp/sql_backup.sql.gz | psql postgres
# pg_restore -v -d commutedb /tmp/sql_backup.sql.gz > /tmp/log
# psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres"
echo "Database restored successfully"