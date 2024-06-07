from datetime import datetime, UTC
from logging import getLogger, INFO, WARNING

from airflow import DAG
from airflow.models import (
    DagRun, )
from polars import DataFrame
from pytest import mark

from clients.s3_client import (
    S3Client,
)
from dags.tests.functions import (
    is_successful,
    clear_dag_run,
    obtain_return_value,
)

logger = getLogger(name=__name__)

engine = 'sqlalchemy.engine'

sqlalchemy_logger = getLogger(
    name=engine,
)


@mark.timeout(timeout=8)
def test_example_dag_not_exists(
    example_dag: DAG,
    s3_client: S3Client,
) -> None:
    formatted = '2024-05-27T00:00:00+00:00'
    logical_date = datetime.fromisoformat(
        formatted,
    )
    template = '/'.join(
        (
            'files', 'year=%Y',
            'month=%m', 'day=%d',
            'date=%Y%m%d',
            f'{formatted}.parquet',
        ),
    )
    key = logical_date.strftime(
        format=template,
    )
    s3_client.delete(key=key)
    clear_dag_run(
        dag=example_dag,
        logical_date=logical_date,
    )
    dag_run: DagRun
    dag_run = example_dag.test(
        execution_date=logical_date,
    )
    assert is_successful(
        dag_run=dag_run,
    ) is True
    logger.info(
        'dag_run_id: %s', dag_run.id,
    )
    value = obtain_return_value(
        dag=example_dag,
        dag_run=dag_run,
        task_id='first',
    )
    assert value == {
        'key': key,
        'exists': False,
    }


@mark.timeout(timeout=8)
def test_example_dag_exists(
    example_dag: DAG,
    s3_client: S3Client,
) -> None:
    logical_date = datetime(
        year=2024, month=5, day=28,
        hour=0, minute=0, second=0,
        microsecond=0, tzinfo=UTC,
    )
    formatted = logical_date.isoformat()
    template = '/'.join(
        (
            'files', 'year=%Y',
            'month=%m', 'day=%d',
            'date=%Y%m%d',
            f'{formatted}.parquet',
        ),
    )
    key = logical_date.strftime(
        format=template,
    )
    numbers = tuple(range(1))
    sample = DataFrame(
        data={
            'integer': numbers,
        },
    )
    s3_client.write_dataframe(
        key=key,
        dataframe=sample,
    )
    clear_dag_run(
        dag=example_dag,
        logical_date=logical_date,
    )
    dag_run = example_dag.test(
        execution_date=logical_date,
    )
    assert is_successful(
        dag_run=dag_run,
    )
    sqlalchemy_logger.setLevel(
        level=INFO,
    )
    logger.info(
        '%s enabled', engine,
    )
    value = obtain_return_value(
        dag=example_dag,
        dag_run=dag_run,
        task_id='first',
    )
    sqlalchemy_logger.setLevel(
        level=WARNING,
    )
    logger.info(
        '%s disabled', engine,
    )
    assert value == {
        'key': key,
        'exists': True,
    }
