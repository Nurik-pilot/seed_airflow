FROM python:3.11.8-slim

ARG FIRST_PART="celery,postgres,sentry"
ARG SECOND_PART="s3,cncf.kubernetes,redis"
ARG EXTENSIONS="$FIRST_PART,$SECOND_PART"
ARG DOMAIN="raw.githubusercontent.com"
ARG BASE_URL="https://$DOMAIN/apache/airflow"
ARG AIRFLOW_VERSION="2.8.3"
ARG PYTHON_VERSION="3.11"
ARG FIRST="constraints-$AIRFLOW_VERSION"
ARG SECOND="constraints-$PYTHON_VERSION"
ARG FILEPATH="$FIRST/$SECOND"

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
    libpq-dev \
    procps \
    netcat-traditional \
# Set timezone
    && echo "UTC" > /etc/timezone \
# Upgrade pip
    && pip install \
    --upgrade pip packaging \
# Add project dependencies
    && pip install \
    apache-airflow[$EXTENSIONS]==$AIRFLOW_VERSION \
    --constraint "$BASE_URL/$FILEPATH.txt" \
    && pip install poetry \
    && poetry install --no-root \
# Remove build dependencies
    && apt purge --yes g++ gcc apt-utils \
    && apt clean autoremove --yes

COPY ./src /src

CMD ["./entrypoint.sh"]
