#!/bin/bash

#Active all env vars for docker compose files
. ./active_dev.sh

docker compose -f ./docker-compose.yaml -f docker-compose.dev.yaml up -d
