set -o allexport
. ./config/uvicorn.prod.env
. ./config/django.prod.env
. ./config/postgres.prod.env
set +o allexport