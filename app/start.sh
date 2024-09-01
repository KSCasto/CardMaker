#!/bin/bash

compose_file="docker-compose.yml"
docker stop card-maker
docker rm card-maker
docker stop nginx
docker rm nginx

if [[ $* == *--prune* ]]; then
    docker system prune -a
fi

# Check if --D flag is provided
if [[ $* == *--K* ]]; then
    compose_file="docker-compose-kubernetes.yml"
fi

if [[ $* == *--L* ]]; then
    compose_file="docker-compose-local.yml"
fi


# Start Docker container
docker-compose -f "$compose_file" up -d --build
docker ps -a
