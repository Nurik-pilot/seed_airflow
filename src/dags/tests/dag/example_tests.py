from airflow import DAG
from airflow.models import (
    DagBag, DagRun,
)
from airflow.utils.state import (
    DagRunState,
)
from pytest import mark

from dags.tests.ignored_warnings import (
    sqlalchemy_warning,
    deprecation_warning,
)


@mark.filterwarnings(
    sqlalchemy_warning,
    deprecation_warning,
)
def test_example_dag(
    dag_bag: DagBag,
) -> None:
    dag: DAG = dag_bag.get_dag(
        dag_id='example',
    )
    dag_run: DagRun = dag.test()
    success = DagRunState.SUCCESS
    assert dag_run.state == success
