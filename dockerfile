FROM python:3.10-alpine

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY multiplex /multiplex
WORKDIR /multiplex
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN adduser --disabled-password multiplex-user

USER multiplex-user