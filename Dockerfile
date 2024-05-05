FROM python:3.12.3-slim

ARG FIRST_PART="celery,postgres,sentry"
ARG SECOND_PART="s3,cncf.kubernetes,redis"
ARG EXTENSIONS="$FIRST_PART,$SECOND_PART"
ARG HOST="https://raw.githubusercontent.com"
ARG URI="apache/airflow"
ARG BASE_URL="$HOST/$URI"
ARG AIRFLOW_VERSION="2.9.0"
ARG PYTHON_VERSION="3.12"
ARG FIRST="constraints-$AIRFLOW_VERSION"
ARG SECOND="constraints-$PYTHON_VERSION"
ARG FILEPATH="$FIRST/$SECOND.txt"
ARG RAW_PACKAGE="apache-airflow[$EXTENSIONS]"
ARG PACKAGE="$RAW_PACKAGE==$AIRFLOW_VERSION"
ARG CONSTRAINT="$BASE_URL/$FILEPATH"

ENV PYTHONUNBUFFERED=1 COLUMNS=200 \
    PYTHONPATH="/src:$PYTHONPATH" \
    PIP_CONFIG_FILE="/src/pip.conf" \
    TZ="UTC" AIRFLOW_HOME="/src"

WORKDIR /src

ADD \
    ./src/poetry.toml \
    ./src/poetry.lock \
    ./src/pyproject.toml \
    ./src/pip.conf \
    /src/

RUN apt update \
    && apt install --yes \
    apt-utils gcc g++ \
    libpq-dev procps \
    netcat-traditional \
# Set timezone
    && echo "UTC" > /etc/timezone \
# Upgrade pip
    && pip install --upgrade pip \
    && pip install $PACKAGE \
    --constraint $CONSTRAINT \
    && pip install poetry \
    && poetry install --no-root \
# Remove build dependencies
    && apt purge --yes \
    g++ gcc apt-utils \
    && apt clean \
    autoremove --yes

COPY ./src /src

CMD ["./entrypoint.sh"]
