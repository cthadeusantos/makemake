export DJANGO_SETTINGS_MODULE=makemake.settings
rm db.sqlite3
find . -type d -name migrations -exec rm -rf {} +
find . -type d -name __pycache__ -exec rm -rf {} +
#python manage.py migrate

python manage.py makemigrations sites
python manage.py makemigrations buildings
python manage.py makemigrations categories
python manage.py makemigrations projects
python manage.py makemigrations documents
python manage.py migrate
python manage.py createsuperuser --username admin