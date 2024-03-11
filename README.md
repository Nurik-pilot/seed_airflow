### Seed

#### For development:
``` $ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs sudo rm -rf ```

``` $ chmod +x src/entrypoint.sh ```

``` $ docker compose up ```

### Run tests:
In separate tab

``` $ docker compose exec web bash ``` - get into airflow_webserver container

``` $ doit lint ``` - run lint

``` $ doit outdated ``` - check outdated

### Test tasks and dags

``` $ airlfow tasks test {dag_id} {task_id} {execution_date}```

``` $ airflow dags test {dag_id} {execution_date} ```
