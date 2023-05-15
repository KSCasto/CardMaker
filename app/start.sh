#!/bin/bash

compose_file="docker-compose.yml"
docker stop app_flask_1
docker rm app_flask_1

# Check if --D flag is provided
if [[ $* == *--D* ]]; then
    compose_file="docker-compose-dev.yml"
fi
if [[ $* == *--L* ]]; then
    compose_file="docker-compose-local.yml"
fi


# Start Docker container
docker-compose -f "$compose_file" up -d
docker ps -a
