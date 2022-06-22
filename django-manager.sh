#!/bin/bash

args=$@
docker compose exec django ./manage.py $args 