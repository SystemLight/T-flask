FROM tiangolo/uwsgi-nginx:python3.7

MAINTAINER SystemLight 1466335092@qq.com

COPY ./src /app
WORKDIR /app
