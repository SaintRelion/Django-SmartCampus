#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Uvicorn..."
uvicorn core.asgi:application --host 0.0.0.0 --port 8000