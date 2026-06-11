FROM python:3.13-slim

LABEL maintainer="rahmanitkd@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY ./core .