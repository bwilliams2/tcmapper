#!/usr/bin/env bash
echo "Restoring database"
gunzip < /tmp/sql_backup.sql.gz | psql -U postgres -h localhost
echo "Database restored successfully"