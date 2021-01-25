#!/usr/bin/env bash
echo "Restoring database"
gunzip < /tmp/sql_backup.sql.gz | psql -u postgres
echo "Database restored successfully"