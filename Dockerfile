FROM alpine:latest

MAINTAINER Bruno Binet <bruno.binet@helioslite.com>

RUN apk add --no-cache py3-tornado py3-magic

ADD tornado /app
WORKDIR /app

EXPOSE 8080

CMD ["python3", "upload.py"]
