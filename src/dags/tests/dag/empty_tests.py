from airflow import DAG
from airflow.models import (
    DagBag, DagRun,
)
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
    dag_bag: DagBag,
) -> None:
    dag: DAG
    dag = dag_bag.get_dag(
        dag_id='empty',
    )
    dag_run: DagRun = dag.test()
    assert is_successful(
        dag_run=dag_run,
    )
