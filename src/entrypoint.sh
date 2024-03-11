#!/bin/bash
# No more than 100 lines of code
wait_for () {
    while ! nc -z "$1" "$2"; do sleep 1; done;
    echo "$1:$2 accepts connections!^_^"
}
wait_backing_services () {
  wait_for "${DB_HOST}" "${DB_PORT}"
  wait_for "${BROKER_HOST}" "${BROKER_PORT}"
}
remove_useless () {
  rm -rf /src/logs celerybeat-schedule \
  airflow-webserver.pid airflow-worker.pid
}

remove_useless

export $(xargs < /src/core/.env)
echo "env variables are populated!^_^"

case "$PROCESS" in
"AIRFLOW_WEBSERVER")
    if [ "$ENV" == "LOCAL" ]; then
      wait_backing_services
      poetry install --no-root
    fi
    airflow db migrate
    if [ "$ENV" == "LOCAL" ]; then
      python setup.py
      airflow users create \
      --username 1 --firstname 1 \
      --lastname 1 --role Admin \
      --email asd@asd.asd --password 1
    fi
    airflow webserver \
    --pid /tmp/airflow-webserver.pid
    ;;
"AIRFLOW_SCHEDULER")
    if [ "$ENV" == "LOCAL" ]; then
      wait_backing_services
      wait_for web 8000
    fi
    airflow db migrate
    echo "setup is done!^_^"
    airflow scheduler
    ;;
"AIRFLOW_CONSUMER")
    if [ "$ENV" == "LOCAL" ]; then
      wait_backing_services
      wait_for web 8000
    fi
    airflow celery worker \
    --pid /tmp/airflow-worker.pid
    ;;
"AIRFLOW_FLOWER")
    if [ "$ENV" == "LOCAL" ]; then
      wait_backing_services
      wait_for web 8000
    fi
    airflow celery flower \
    --basic-auth=1:1
    ;;
"TEST")
    wait_backing_services
    airflow db migrate \
    && python setup.py \
    && airflow users create \
    --username 1 --password 1 \
    --firstname 1 --lastname 1 \
    --email asd@asd.asd --role Admin \
    && doit test \
    --number_of_processes 2 \
    --coverage_report_path \
    "$CI_PROJECT_DIR"/src/cov.xml \
    && doit lint
    ;;
"SCAN")
    base_url="https://raw.githubusercontent.com"
    url="$base_url"/anchore/grype/main/install.sh
    doit safety \
    && apt install --yes curl \
    && curl -sSfL $url | sh -s -- -b /usr/local/bin \
    && grype --fail-on CRITICAL .
    ;;
*)
    echo "NO PROCESS SPECIFIED!>_<"
    exit 1
    ;;
esac
