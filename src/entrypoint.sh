#!/bin/bash
# No more than 100 lines of code
wait_for () {
    while ! nc -z "$1" "$2"
    do
      sleep 1
    done
    echo "$1:$2 is ready!^_^"
}

wait_backing_services () {
  wait_for "${DB_HOST}" "${DB_PORT}"
  wait_for "${BROKER_HOST}" "${BROKER_PORT}"
}

create_test_user () {
  airflow users create \
  --username 1 --password 1 \
  --firstname 1 --lastname 1 \
  --role Admin --email asd@asd.asd
}

set -o allexport
source /src/core/.env
set +o allexport
echo "env variables are populated!^_^"

case "$PROCESS" in
"AIRFLOW_WEBSERVER")
    if [ "$ENV" == "LOCAL" ]
    then
      wait_backing_services
      poetry install
    fi
    airflow db migrate
    python setup.py
    if [ "$ENV" == "LOCAL" ]
    then
      create_test_user
    fi
    airflow webserver --pid \
    /tmp/airflow-webserver.pid
    ;;
"AIRFLOW_SCHEDULER")
    if [ "$ENV" == "LOCAL" ]
    then
      wait_for web 8000
    fi
    airflow db migrate
    echo "setup is done!^_^"
    airflow scheduler --pid \
    /tmp/airflow-scheduler.pid
    ;;
"AIRFLOW_CONSUMER")
    if [ "$ENV" == "LOCAL" ]
    then
      wait_for web 8000
    fi
    airflow celery worker \
    --pid /tmp/airflow-worker.pid
    ;;
"AIRFLOW_FLOWER")
    if [ "$ENV" == "LOCAL" ]
    then
      wait_for web 8000
    fi
    airflow celery flower \
    --basic-auth "1:1"
    ;;
"TEST")
    wait_backing_services
    airflow db migrate \
    && python setup.py \
    && create_test_user \
    && doit test \
    --number_of_processes 1 \
    --coverage_report_path \
    "$CI_PROJECT_DIR"/src/cov.xml \
    && doit lint
    ;;
"SCAN")
    domain="raw.githubusercontent.com"
    path="anchore/grype/main"
    file="install.sh"
    url="https://$domain/$path/$file"
    echo "url: $url"
    doit safety \
    && apt install --yes curl \
    && curl -sSfL $url >> $file \
    && sh $file -b /usr/local/bin \
    && grype . --fail-on CRITICAL
    ;;
*)
    echo "NO PROCESS SPECIFIED!>_<"
    exit 1
    ;;
esac
