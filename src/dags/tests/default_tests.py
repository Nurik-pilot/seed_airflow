from airflow import DAG
from airflow.models import (
    DagBag, DagRun, Connection,
)
from airflow.settings import Session
from airflow.utils.state import (
    DagRunState,
)
from pytest import mark
from sqlalchemy.orm import Query

from dags.tests.ignored_warnings import (
    pytest_warning,
    sqlalchemy_warning,
    deprecation_warning,
)
from setup import setup_s3_connection


def test_no_import_errors(
    dag_bag: DagBag,
) -> None:
    assert len(
        dag_bag.import_errors,
    ) == 0


def test_dag_ids(
    dag_bag: DagBag,
) -> None:
    assert dag_bag.dag_ids == [
        'empty', 'example',
    ]


def test_dags_count(
    dag_bag: DagBag,
) -> None:
    assert dag_bag.size() == 2


def test_connection() -> None:
    query: Query
    with (
        Session() as session,
        session.begin(),
    ):
        query = session.query(
            Connection,
        )
        query.delete()
        assert query.count() == 0
    setup_s3_connection()
    with Session() as session:
        query = session.query(
            Connection,
        )
        assert query.count() == 1


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


@mark.filterwarnings(
    sqlalchemy_warning,
    deprecation_warning,
)
def test_example_dag(
    dag_bag: DagBag,
) -> None:
    dag: DAG
    dag = dag_bag.get_dag(
        dag_id='example',
    )
    dag_run: DagRun = dag.test()
    success = DagRunState.SUCCESS
    assert dag_run.state == success
