FROM debian:bullseye

MAINTAINER Bruno Binet <bruno.binet@helioslite.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install -yq --no-install-recommends \
    curl openssh-server python3-tornado python3-magic \
  && rm -rf /var/lib/apt/lists/*

ADD tornado /app
WORKDIR /app

EXPOSE 8080

CMD ["python3", "upload.py"]
