set -o allexport
. ./config/gunicorn.prod.env
. ./config/django.prod.env
. ./config/postgres.prod.env
set +o allexport