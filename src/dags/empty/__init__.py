from datetime import datetime, UTC

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

from .bash_commands import (
    echo_hello_world,
)
from .python_callables import (
    print_hello_world,
)

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
    second = BashOperator(
        task_id='second',
        bash_command=echo_hello_world,
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
