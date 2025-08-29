#!/bin/bash
set -e

echo "🔄 Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -p 5432 -U postgres; do
    echo "⏳ PostgreSQL is unavailable - sleeping"
    sleep 2
done

echo "✅ PostgreSQL is ready!"

echo "🔄 Running database migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI service..."
cd src
exec fastapi dev main.py --host 0.0.0.0 --port 8000
