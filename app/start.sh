#!/bin/bash

compose_file="docker-compose.yml"

# Check if --D flag is provided
if [[ $* == *--D* ]]; then
    compose_file="docker-compose-dev.yml"
fi
if [[ $* == *--L* ]]; then
    compose_file="docker-compose-local.yml"
fi


# Start Docker container
docker-compose -f "$compose_file" up -d
