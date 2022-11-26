pipenv run python3.9 manage.py collectstatic  --noinput
pipenv run python3.9 manage.py migrate

pipenv run python3.9 manage.py runserver 0.0.0.0:8000
