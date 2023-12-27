#!/bin/sh

echo "Running migrations"
alembic upgrade head
echo "Migrations complete"

echo "Starting Uvicorn with live reload"
uvicorn shared.core.server:app --reload --workers 1 --host 0.0.0.0 --port 8000
