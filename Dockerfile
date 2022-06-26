FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add musl-dev wget
RUN apk add gcc make g++ zlib-dev
RUN pip3 install --upgrade pip
RUN pip3 install cython

WORKDIR /insiderweek

COPY . ./

RUN pip3 install -r requirements.txt