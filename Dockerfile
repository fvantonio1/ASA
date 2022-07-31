FROM ubuntu:20.04

EXPOSE 5000

ENV DATABASE_URL="postgresql://postgres:postgres@172.18.0.3:5432/asa"\
    POSTGRES_PASSWORD="postgres"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

RUN apt -y update \
    && apt install -y \
    libpq-dev \
    apt-utils \
    tzdata \
    apt-transport-https \
    build-essential \
    python3.8 -y \
    python3-dev \
    python3-pip \
    sqlite3 \
    software-properties-common -y 

WORKDIR /app
ADD . /app
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt


CMD ["python3", "app.py"]


