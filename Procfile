release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn django_rest_chat.wsgi  --log-file -