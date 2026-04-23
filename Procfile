web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_db data.csv --with-feedback && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
