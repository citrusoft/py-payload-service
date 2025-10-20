#!/usr/bin/env bash
set -euo pipefail

# Default DATABASE_URL if not provided
: "${DATABASE_URL:=sqlite+aiosqlite:///./dev.db}"

export DATABASE_URL

# Run alembic migrations if alembic is available
if command -v alembic >/dev/null 2>&1; then
  echo "Running alembic upgrade head..."
  alembic upgrade head || echo "alembic upgrade head failed"
else
  echo "alembic not found; skipping migrations"
fi

# Exec the provided command (uvicorn by default)
exec "$@"
