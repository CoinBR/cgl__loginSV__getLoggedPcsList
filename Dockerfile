FROM python:3.8.1-alpine3.11
RUN apk update

WORKDIR /usr/src/app

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
