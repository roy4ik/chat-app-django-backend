release: python manage.py makemigrations accounts
release: python manage.py migrate accounts
release: python manage.py makemigrations chat
release: python manage.py migrate chat

web: gunicorn django_rest_chat.wsgi  --log-file -