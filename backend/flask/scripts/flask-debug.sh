#!/bin/bash

# Set environment variables
export FLASK_APP=flask/app.py
export FLASK_DEBUG=1
export FLASK_RUN_CERT=flask/ssl_cert/localhost.pem
export FLASK_RUN_KEY=flask/ssl_cert/localhost-key.pem
export GOAUTH_CLIENT_ID
export GOAUTH_CLIENT_SECRET

# Start the Flask application
flask run --host=127.0.0.1 --port=5235
