#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_ready() {
  poetry run python <<END
import sys

import psycopg2
import os

try:
    psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port=5432
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  echo >&2 'Waiting for PostgreSQL to become available...'
  sleep 1
done
echo >&2 'PostgreSQL is available'
logs_dir_exist() {
  poetry run python <<END
import os
if os.path.exists('logs') is False:
    os.mkdir('logs')
    print('create logs directory')
else:
    print('logs directory already exist')
END
  echo '===== local logs checked ====='
}
logs_dir_exist
poetry run flask db upgrade
poetry run python app.py
#poetry run gunicorn app:app -b 0.0.0.0:5000 --worker-class gevent --log-level INFO --reload
