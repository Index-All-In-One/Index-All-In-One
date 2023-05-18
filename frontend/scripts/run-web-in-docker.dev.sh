#!/bin/bash

export DOMAIN_NAME=${DOMAIN_NAME:-"localhost"}
export GOAUTH_CLIENT_ID

# run this script from the root of frontend
./scripts/build-web-release.sh

docker build -f docker-nginx/Dockerfile.dev -t iaio-flutter-web .
docker run -d --rm --name iaio-flutter-web-debug -p 8000:443 -e GOAUTH_CLIENT_ID=$GOAUTH_CLIENT_ID iaio-flutter-web
