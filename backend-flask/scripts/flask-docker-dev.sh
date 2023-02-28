#!/bin/bash

# Set environment variables
export FLASK_APP=Index-All-In-One-Flask
export FLASK_DEBUG=1

# Start the Flask application
flask run --host=0.0.0.0 --port=5235
