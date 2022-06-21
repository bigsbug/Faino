set -o allexport
. ./uvicorn.dev.env
. ./django.dev.env
. ./postgres.dev.env
set +o allexport