from datetime import datetime
from logging import getLogger

from airflow import DAG
from airflow.models import (
    DagRun, Variable,
)
from polars import DataFrame
from pyarrow.fs import (
    S3FileSystem,
)
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


@mark.timeout(timeout=8)
def test_example_dag_not_exists(
    example_dag: DAG,
    s3_client: S3Client,
) -> None:
    formatted = '2024-05-27T00:00:00+00:00'
    logical_date = datetime.fromisoformat(
        formatted,
    )
    bucket = 'seed'
    template = '/'.join(
        (
            'files', 'year=%Y', 'month=%m',
            'day=%d', 'date=%Y%m%d',
            f'{formatted}.parquet',
        ),
    )
    key = logical_date.strftime(
        format=template,
    )
    s3_client.delete(
        bucket=bucket, key=key,
    )
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
        'bucket': bucket,
        'key': key,
        'exists': False,
    }


@mark.timeout(timeout=8)
def test_example_dag_exists(
    example_dag: DAG,
) -> None:
    formatted = '2024-05-28T00:00:00+00:00'
    logical_date = datetime.fromisoformat(
        formatted,
    )
    bucket = 'seed'
    template = '/'.join(
        (
            'files', 'year=%Y', 'month=%m',
            'day=%d', 'date=%Y%m%d',
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
    login = Variable.get(
        key='s3_login',
    )
    password = Variable.get(
        key='s3_password',
    )
    host = Variable.get(
        key='s3_host',
    )
    filesystem = S3FileSystem(
        access_key=login,
        secret_key=password,
        endpoint_override=host,
    )
    destination = '/'.join(
        (bucket, key,),
    )
    with filesystem.open_output_stream(
        path=destination,
    ) as stream:
        sample.write_parquet(
            file=stream,
            use_pyarrow=True,
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
    ) is True
    value = obtain_return_value(
        dag=example_dag,
        dag_run=dag_run,
        task_id='first',
    )
    assert value == {
        'bucket': bucket,
        'key': key,
        'exists': True,
    }
