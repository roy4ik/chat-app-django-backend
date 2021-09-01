release: python manage.py makemigrations
release: python manage.py migrate

web: DJANGO_SETTINGS_MODULE=django_rest_chat.prod_settings gunicorn django-rest-chat.wsgi  --log-file -