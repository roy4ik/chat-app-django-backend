release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn django-rest-chat.wsgi  --log-file -