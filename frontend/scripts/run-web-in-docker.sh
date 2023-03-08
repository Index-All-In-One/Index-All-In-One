#!/bin/bash

# run this script from the root of frontend
./scripts/build-web-release.sh

docker build -f docker-nginx/Dockerfile -t flutter-web .
docker run -d --rm --name flutter-web-debug -p 8000:80 flutter-web
