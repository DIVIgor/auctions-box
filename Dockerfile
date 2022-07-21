FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# # pull oggivisl base image
# FROM python:3.10-alpine

# # set work directory
# WORKDIR /app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV DEBUG 0

# # -I think it's not necessary-
# # install psycopg2
# RUN apk update \
#     && apk add --virtual build-essential gcc python3-dev musl-dev \
#     && apk add postgresql-dev \
#     && pip install psycopg2

# # install dependencies
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# # copy project
# COPY . .

# # add and run as non-root user
# RUN adduser -D myuser
# USER myuser

# # run gunicorn
# CMD gunicorn commerce.wsgi:application --bind 0.0.0.0:$PORT