from datetime import datetime, UTC

from airflow import DAG
from airflow.operators.python import (
    PythonOperator,
)

from .python_callables import (
    write_example_parquet,
)

with DAG(
    dag_id='example',
    schedule='@hourly',
    max_active_runs=4,
    start_date=datetime(
        year=2024, month=5, day=1,
        hour=0, minute=0, second=0,
        microsecond=0, tzinfo=UTC,
    ),
):
    first = PythonOperator(
        task_id='first',
        python_callable=write_example_parquet,
    )
