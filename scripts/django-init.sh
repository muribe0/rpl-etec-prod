#!/bin/bash
set -e

# Wait for database
echo "Waiting for database..."
./scripts/wait-for-it.sh db:5432

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the command passed to this script
echo "Starting application..."
exec "$@"