#!/usr/bin/env bash
echo "Restoring database"
# gunzip < /tmp/sql_backup.sql.gz | psql -U postgres
gunzip -c /tmp/sql_backup.sql.gz > /tmp/sql_backup.sql
# psql -U postgres postgres < /tmp/sql_backup.sql 
psql -f /tmp/sql_backup.sql postgres

echo "Database restored successfully"