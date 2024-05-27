from airflow import DAG
from airflow.models import (
    DagBag, DagRun,
)
from pytest import mark

from dags.tests.functions import (
    is_successful,
)


@mark.timeout(timeout=8)
def test_example_dag(
    dag_bag: DagBag,
) -> None:
    dag: DAG
    dag = dag_bag.get_dag(
        dag_id='example',
    )
    dag_run: DagRun = dag.test()
    assert is_successful(
        dag_run=dag_run,
    )
