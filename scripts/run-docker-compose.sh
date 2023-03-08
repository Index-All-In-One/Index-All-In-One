#!/bin/bash

# run this script from the root of whole project

# set up environment variables
export SERVER_URL=${SERVER_URL:-"http://127.0.0.1:8000"}
export LOCAL_ADDR=${LOCAL_ADDR:-"127.0.0.1:8000"}
export BACKEND_LOCAL_PORT=${BACKEND_LOCAL_PORT:-"5235"}
export FLUTTER_BASE_URL="$SERVER_URL/api"

# build frontend web release
cd frontend
./scripts/build-web-release.sh
cd ..

docker-compose -f docker-compose/docker-compose.yml up --build
