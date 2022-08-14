release: python manage.py migrate
web: gunicorn woodniture.wsgi --log-file=-
python manage.py collectstatic --noinput
