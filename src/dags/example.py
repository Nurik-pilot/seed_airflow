from datetime import datetime, UTC
from logging import getLogger
from uuid import uuid4

from airflow import DAG
from airflow.models import Connection
from airflow.operators.python import (
    PythonOperator,
)
from airflow.settings import Session
from numpy.random import default_rng
from orjson import loads
from pandas import DataFrame
from sqlalchemy import select
from sqlalchemy.orm import load_only

logger = getLogger(name=__name__)


def example() -> str:
    sample: DataFrame = DataFrame(
        data=default_rng().integers(
            low=0, high=100,
            size=(100, 4,),
        ),
        columns=(
            'A', 'B', 'C', 'D',
        ),
    )
    with (
        Session() as session,
        session.begin(),
    ):
        statement = select(
            Connection,
        ).options(
            load_only(
                Connection.extra,
            ),
        )
        connection = session.scalars(
            statement=statement,
        ).one()
        data = loads(connection.extra)
    filename = str(uuid4())
    now = datetime.now(tz=UTC)
    bucket = 'seed'
    folder = 'files'
    partition = '%Y/%m/%d'
    formatted = '/'.join(
        (
            bucket, folder,
            partition, filename,
        ),
    )
    upload_to = now.strftime(
        format=f's3://{formatted}.parquet',
    )
    storage_options = {
        'key': data['aws_access_key_id'],
        'secret': data['aws_secret_access_key'],
        'endpoint_url': data['endpoint_url'],
        'use_ssl': False,
    }
    sample.to_parquet(
        path=upload_to, engine='pyarrow',
        storage_options=storage_options,
    )
    return upload_to


with DAG(
    dag_id='example',
    schedule='@daily',
    start_date=datetime(
        year=2024, month=5, day=13,
        hour=0, minute=0, second=0,
        microsecond=0, tzinfo=UTC,
    ),
):
    first_task = PythonOperator(
        task_id='first_task',
        python_callable=example,
    )
