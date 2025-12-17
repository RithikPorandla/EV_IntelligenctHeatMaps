#!/bin/bash

# Database initialization script
# This script waits for the database to be ready and initializes tables

set -e

echo "Waiting for database to be ready..."

# Wait for PostgreSQL to be ready
until PGPASSWORD=evcharge123 psql -h db -U evcharge -d evcharge -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up - initializing database"

# Initialize database tables via backend
cd /app
python -c "from app.database import init_db; init_db()"

echo "Database initialized successfully"
