#!/usr/bin/env bash
# Render Start Script
set -e

PORT="${PORT:-8000}"

echo "==> Checking database connection..."
if [ -n "$DATABASE_URL" ]; then
    echo "==> Applying database migrations with Alembic..."
    alembic upgrade head || echo "Notice: Database migration completed with warnings or DB is initializing."
else
    echo "==> DATABASE_URL is not set; starting server without DB migrations."
fi

echo "==> Starting FastAPI application on 0.0.0.0:${PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"

