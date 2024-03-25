from datetime import datetime, UTC
from logging import getLogger

from airflow import DAG
from airflow.operators.bash import (
    BashOperator,
)
from airflow.operators.empty import (
    EmptyOperator,
)
from airflow.operators.python import (
    PythonOperator,
)

logger = getLogger(name=__name__)


def print_hello_world() -> None:
    message = ' '.join(
        (
            'hello world by',
            'PythonOperator',
        ),
    )
    logger.info(msg=message)


with DAG(
    dag_id='empty',
    schedule='@daily',
    start_date=datetime(
        year=2024, month=3,
        day=20, tzinfo=UTC,
    ),
):
    first_task = EmptyOperator(
        task_id='first_task',
    )
    bash_command = ' '.join(
        (
            'echo hello',
            'world by',
            'BashOperator',
        ),
    )
    second_task = BashOperator(
        task_id='second_task',
        bash_command=bash_command,
    )
    third_task = PythonOperator(
        task_id='third_task',
        python_callable=print_hello_world,
    )

    first_task >> second_task >> third_task
