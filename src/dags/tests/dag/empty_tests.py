from airflow import DAG
from airflow.models import DagRun
from pytest import mark

from dags.tests.functions import (
    is_successful,
)
from dags.tests.ignored import (
    pytest_warning,
)


@mark.filterwarnings(
    pytest_warning,
)
def test_empty_dag(
    empty_dag: DAG,
) -> None:
    dag_run: DagRun
    dag_run = empty_dag.test()
    assert is_successful(
        dag_run=dag_run,
    )
