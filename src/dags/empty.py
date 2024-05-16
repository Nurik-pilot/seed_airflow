from datetime import datetime, UTC
from logging import getLogger
from typing import Any

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


def print_hello_world(
    logical_date: datetime,
    **kwargs: dict[str, Any],
) -> None:
    logger.info(
        'logical_date: %s',
        logical_date.isoformat(),
    )
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
    max_active_runs=4,
    start_date=datetime(
        year=2024, month=5, day=1,
        hour=0, minute=0, second=0,
        microsecond=0, tzinfo=UTC,
    ),
):
    first = EmptyOperator(
        task_id='first',
    )
    bash_command = ' '.join(
        (
            'echo hello',
            'world by',
            'BashOperator',
        ),
    )
    second = BashOperator(
        task_id='second',
        bash_command=bash_command,
    )
    third = PythonOperator(
        task_id='third',
        python_callable=print_hello_world,
    )

    first.set_downstream(
        task_or_task_list=second,
    )
    second.set_downstream(
        task_or_task_list=third,
    )
