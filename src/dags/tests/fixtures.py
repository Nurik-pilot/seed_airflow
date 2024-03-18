from airflow.models import DagBag
from pytest import fixture


@fixture()
def dag_bag() -> DagBag:
    return DagBag(
        dag_folder='/src/dags/',
        include_examples=False,
    )
