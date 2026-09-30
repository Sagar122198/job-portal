#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python manage.py shell -c "
from account.models import CustomUser
if not CustomUser.objects.filter(is_superuser=True).exists():
    CustomUser.objects.create_superuser('admin', 'admin@jobportal.com', '${DJANGO_SUPERUSER_PASSWORD:-admin123}')
    print('Superuser created.')
else:
    print('Superuser already exists.')
"

echo "Starting gunicorn..."
exec gunicorn job_portal.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --timeout 120
