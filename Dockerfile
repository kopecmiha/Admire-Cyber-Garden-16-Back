# pull official base image
FROM python:3.9.9-slim
# set work directory
WORKDIR /app
# set environment variables
ARG DATABASE_NAME
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ARG DATABASE_HOST
ARG DATABASE_PORT

ENV DATABASE_NAME=$DATABASE_NAME
ENV DATABASE_USER=$DATABASE_USER
ENV DATABASE_PASSWORD=$DATABASE_PASSWORD
ENV DATABASE_HOST=$DATABASE_HOST
ENV DATABASE_PORT=$DATABASE_PORT
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN python3.9 -m pip install pipenv

COPY . .

RUN pipenv install -d --pre

#RUN echo "DATABASE_NAME=$DATABASE_NAME" > .env
#RUN echo "DATABASE_USER=$DATABASE_USER" >> .env
#RUN echo "DATABASE_PASSWORD=$DATABASE_PASSWORD" >> .env
#RUN echo "DATABASE_HOST=$DATABASE_HOST" >> .env
#RUN echo "DATABASE_PORT=$DATABASE_HOST" >> .env
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh" ]
