FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /carbonusage

WORKDIR /carbonusage

COPY . .

COPY ./requirements.txt /requirements.txt

RUN apk add --update postgresql-client jpeg-dev
RUN apk add --update --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r requirements.txt