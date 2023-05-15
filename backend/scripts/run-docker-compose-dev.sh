#!/bin/bash

# set up environment variables
export GOAUTH_CLIENT_ID
export GOAUTH_CLIENT_SECRET
DOCKER_DEV_FILE_NAME=${DOCKER_DEV_FILE_NAME:-"default"}

action="run" # set default behavior to "run"

if [[ $# -gt 0 ]]; then
  case $1 in
    run)
        action="run"
        ;;
    stop)
        action="stop"
        ;;
    clean)
        action="clean"
        ;;
    logs)
        action="logs"
        ;;
    rebuild)
        action="rebuild"
        ;;
    *)
        echo "Invalid operation: $1"
        exit 1
        ;;
  esac
fi

if [[ $action == "run" ]]; then

    echo "Running docker-compose"

    docker-compose -f docker-compose/docker-compose.dev.$DOCKER_DEV_FILE_NAME.yml up -d --build
elif [[ $action == "stop" ]]; then
    echo "Stopping docker-compose"

    docker-compose -f docker-compose/docker-compose.dev.$DOCKER_DEV_FILE_NAME.yml down
elif [[ $action == "clean" ]]; then
    echo "Cleaning docker-compose"

    docker-compose -f docker-compose/docker-compose.dev.$DOCKER_DEV_FILE_NAME.yml down --volumes --remove-orphans
elif [[ $action == "logs" ]]; then
    echo "Showing docker-compose logs $2"

    docker-compose -f docker-compose/docker-compose.dev.$DOCKER_DEV_FILE_NAME.yml logs --follow $2
elif [[ $action == "rebuild" ]]; then
    echo "Rebuilding docker-compose service $2"

    docker-compose -f docker-compose/docker-compose.dev.$DOCKER_DEV_FILE_NAME.yml build $2
    docker-compose -f docker-compose/docker-compose.dev.$DOCKER_DEV_FILE_NAME.yml restart $2
fi
