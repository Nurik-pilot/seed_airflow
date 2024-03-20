from airflow.models import DagBag
from pytest import fixture


@fixture()
def dag_bag() -> DagBag:
    instance = DagBag(
        dag_folder='/src/dags/',
        include_examples=False,
    )
    instance.sync_to_db()
    return instance
