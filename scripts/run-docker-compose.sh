#!/bin/bash

# run this script from the root of whole project

# set up environment variables
export FLUTTER_BASE_URL="http://localhost:8000/api"

# build frontend web release
cd frontend
./scripts/build-web-release.sh
cd ..

docker-compose -f docker-compose/docker-compose.yml up --build
