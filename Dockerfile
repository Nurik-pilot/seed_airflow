FROM python:3.12.3-slim

ARG AIRFLOW_VERSION="2.9.1"
ARG PYTHON_VERSION="3.12"
ARG PACKAGE="apache-airflow[celery,postgres,sentry,s3,cncf.kubernetes,virtualenv]==$AIRFLOW_VERSION"
ARG CONSTRAINT="https://raw.githubusercontent.com/apache/airflow/constraints-$AIRFLOW_VERSION/constraints-$PYTHON_VERSION.txt"

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
    && poetry install \
# Remove build dependencies
    && apt purge --yes \
    g++ gcc apt-utils \
    && apt clean \
    autoremove --yes

COPY ./src /src

CMD ["./entrypoint.sh"]
