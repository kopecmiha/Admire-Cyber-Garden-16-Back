FROM python:3.9.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN python3.9 -m pip install pipenv

COPY Pipfile .
RUN pipenv install -d --pre

COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh" ]
