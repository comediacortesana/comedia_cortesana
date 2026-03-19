#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   SOURCE_DB_URL="postgresql://..." TARGET_DB_URL="postgresql://..." ./scripts/migrate_supabase_to_postgres.sh
# Optional:
#   TABLES="autores lugares obras representaciones" ./scripts/migrate_supabase_to_postgres.sh

if [[ -z "${SOURCE_DB_URL:-}" ]]; then
  echo "ERROR: SOURCE_DB_URL is required"
  exit 1
fi

if [[ -z "${TARGET_DB_URL:-}" ]]; then
  echo "ERROR: TARGET_DB_URL is required"
  exit 1
fi

if ! command -v pg_dump >/dev/null 2>&1; then
  echo "ERROR: pg_dump not found. Install PostgreSQL client tools."
  exit 1
fi

if ! command -v psql >/dev/null 2>&1; then
  echo "ERROR: psql not found. Install PostgreSQL client tools."
  exit 1
fi

DUMP_FILE="${DUMP_FILE:-/tmp/comedias_migration_$(date +%Y%m%d_%H%M%S).dump}"

echo "==> Exporting schema+data from source (Supabase)..."
if [[ -n "${TABLES:-}" ]]; then
  TABLE_ARGS=()
  for table in ${TABLES}; do
    TABLE_ARGS+=("--table=${table}")
  done
  pg_dump --format=custom --no-owner --no-privileges "${TABLE_ARGS[@]}" "${SOURCE_DB_URL}" > "${DUMP_FILE}"
else
  pg_dump --format=custom --no-owner --no-privileges "${SOURCE_DB_URL}" > "${DUMP_FILE}"
fi

echo "==> Restoring dump into target PostgreSQL..."
pg_restore --clean --if-exists --no-owner --no-privileges --dbname="${TARGET_DB_URL}" "${DUMP_FILE}"

echo "==> Running Django migrations on target to finalize schema ownership..."
python manage.py migrate

echo "==> Done. Dump file: ${DUMP_FILE}"
