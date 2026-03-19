#!/bin/sh

echo "LOG: Waiting for database..."

sleep 5

echo "LOG: Running migrations..."

alembic upgrade head

echo "LOG: Starting server..."

uvicorn app.main:app --host 0.0.0.0 --port 8000