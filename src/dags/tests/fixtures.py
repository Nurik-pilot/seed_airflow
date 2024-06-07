from airflow import DAG
from airflow.models import DagBag, Variable
from pytest import fixture

from clients.s3_client import S3Client


@fixture(scope='session')
def dag_bag() -> DagBag:
    return DagBag(
        dag_folder='/src/dags/',
        include_examples=False,
    )


@fixture(scope='session')
def empty_dag(
    dag_bag: DagBag,
) -> DAG:
    return dag_bag.get_dag(
        dag_id='empty',
    )


@fixture(scope='session')
def example_dag(
    dag_bag: DagBag,
) -> DAG:
    return dag_bag.get_dag(
        dag_id='example',
    )


@fixture()
def s3_client() -> S3Client:
    login = Variable.get(
        key='s3_login',
    )
    password = Variable.get(
        key='s3_password',
    )
    host = Variable.get(
        key='s3_host',
    )
    bucket = Variable.get(
        key='s3_bucket',
    )
    return S3Client(
        login=login,
        password=password,
        host=host,
        bucket=bucket,
    )
