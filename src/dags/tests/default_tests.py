from airflow.models import (
    DagBag, Connection,
)
from airflow.settings import Session
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
    assert len(dag_bag.dags) == 1


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


def test_empty_dag(dag_bag: DagBag) -> None:
    dag = dag_bag.dags['empty']
    dag.test()
