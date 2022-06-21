set -o allexport
. ./config/uvicorn.dev.env
. ./config/django.dev.env
. ./config/postgres.dev.env
set +o allexport