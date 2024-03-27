from airflow.models import (
    DagBag, Connection, DagRun,
)
from airflow.settings import Session
from airflow.utils.state import DagRunState
from sqlalchemy.orm import Query

from setup import setup_s3_connection


def test_no_import_errors(
    dag_bag: DagBag,
) -> None:
    assert len(
        dag_bag.import_errors,
    ) == 0


def test_dags_count(
    dag_bag: DagBag,
) -> None:
    assert dag_bag.size() == 1


def test_connection() -> None:
    query: Query
    with Session() as session, session.begin():
        query = session.query(Connection)
        query.delete()
        assert query.count() == 0
    setup_s3_connection()
    with Session() as session:
        query = session.query(Connection)
        assert query.count() == 1


def test_empty_dag(
    dag_bag: DagBag,
) -> None:
    kwargs = {
        'dag_id': 'empty',
    }
    dag = dag_bag.get_dag(**kwargs)
    dag_run: DagRun = dag.test()
    state = dag_run.state
    successful = DagRunState.SUCCESS
    assert state == successful
