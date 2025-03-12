#!/bin/bash
echo "Installing missing dependencies..."
pip install --user gunicorn
echo "Starting application..."
gunicorn app:app

