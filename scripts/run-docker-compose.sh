#!/bin/bash

# run this script from the root of whole project

# set up environment variables
export SERVER_URL=${SERVER_URL:-"http://127.0.0.1:8000"}
export LOCAL_ADDR=${LOCAL_ADDR:-"127.0.0.1:8000"}
export BACKEND_LOCAL_PORT=${BACKEND_LOCAL_PORT:-"5235"}
export FLUTTER_BASE_URL="$SERVER_URL/api"

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
    *)
        echo "Invalid operation: $1"
        exit 1
        ;;
  esac
fi


if [[ $action == "run" ]]; then
    echo "Building frontend web release"

    # build frontend web release
    cd frontend
    ./scripts/build-web-release.sh
    cd ..

    echo "Running docker-compose"

    docker-compose -f docker-compose/docker-compose.yml up -d --build
elif [[ $action == "stop" ]]; then
    echo "Stopping docker-compose"

    docker-compose -f docker-compose/docker-compose.yml down
elif [[ $action == "clean" ]]; then
    echo "Cleaning docker-compose"

    docker-compose -f docker-compose/docker-compose.yml down --volumes --remove-orphans
elif [[ $action == "logs" ]]; then
    echo "Showing docker-compose logs $2"

    docker-compose -f docker-compose/docker-compose.yml logs --follow $2
fi
