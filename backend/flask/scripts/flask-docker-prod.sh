#!/bin/bash

# Set environment variables
export FLASK_APP=flask/app.py
export FLASK_DEBUG=0

# Start the Flask application
flask run --host=0.0.0.0 --port=5235
