#!/bin/bash

# Set environment variables
export FLASK_APP=flask/app.py
export FLASK_DEBUG=1

# Start the Flask application
flask run --host=127.0.0.1 --port=5235
