from airflow import DAG
from airflow.models import (
    DagBag, DagRun,
)
from airflow.utils.state import (
    DagRunState,
)
from pytest import mark

from dags.tests.ignored_warnings import (
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
    success = DagRunState.SUCCESS
    assert dag_run.state == success
