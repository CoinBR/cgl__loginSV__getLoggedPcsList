FROM python:3.8.1-buster
RUN apt-get update

WORKDIR /usr/src/app

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
