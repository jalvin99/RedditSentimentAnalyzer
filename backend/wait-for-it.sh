#!/usr/bin/env bash
# wait-for-it.sh

set -e

host="db" # The service name in docker-compose
user="postgres" # The PostgreSQL username
password="bZm01ql!" # The PostgreSQL password

until PGPASSWORD=$password psql -h "$host" -U "$user" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command: $@"
exec "$@"