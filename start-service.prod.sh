#!/bin/bash

#Active all env vars for docker compose files
. ./active_prod.sh

docker compose -f ./docker-compose.yaml -f docker-compose.prod.yaml up -d
