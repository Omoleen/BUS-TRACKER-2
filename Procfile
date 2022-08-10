release: python3 manage.py migrate
web: daphne Bustracker.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=Bustracker.settings -v2