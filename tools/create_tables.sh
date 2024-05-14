#!/bin/bash
echo "Export enviroment variables"
export DJANGO_SETTINGS_MODULE=makemake.settings

echo "Delete .sqlite3 database"
rm db.sqlite3

echo "Cleaning migrations folders"
#find . -type d -name migrations -exec rm -rf {} +
#find . -type d -name "migrations" -exec find {} -type f -regex '.*/[0-9]\{4,\}_initial.py' -delete \;
#find . -type d -name "migrations" -exec find {} -type f ! -name "__init__.py" -delete \;
find . \( -name ".env" -o -name "env" -o -name "venv" -o -name ".venv" \) -prune -o -type d -name "migrations" -exec find {} -type f ! -name "__init__.py" -delete \;


echo "Delete __pycache__ folders"
#find . -type d -name __pycache__ -exec rm -rf {} +;
find . -type d \( -name ".env" -o -name "env" -o -name "venv" -o -name ".venv" \) -prune -o -type d -name "__pycache__" -exec rm -rf {} +

echo "Running makemigrations"
python manage.py makemigrations

echo "Running migrate"
python manage.py migrate

echo "Create superuser"
python manage.py createsuperuser --username admin