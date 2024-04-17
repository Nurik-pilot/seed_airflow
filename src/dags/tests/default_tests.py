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
    with (
        Session() as session,
        session.begin(),
    ):
        query = session.query(Connection)
        query.delete()
        assert query.count() == 0
    setup_s3_connection()
    with Session() as session:
        query = session.query(Connection)
        assert query.count() == 1


warning = '::'.join(
    (
        'ignore', '.'.join(
            (
                'pytest', ''.join(
                    (
                        'PytestUnraisable',
                        'ExceptionWarning',
                    ),
                ),
            ),
        ),
    ),
)


@mark.filterwarnings(warning)
def test_empty_dag(
    dag_bag: DagBag,
) -> None:
    kwargs: dict[str, str] = {
        'dag_id': 'empty',
    }
    dag: DAG
    dag = dag_bag.get_dag(**kwargs)
    dag_run: DagRun = dag.test()
    success = DagRunState.SUCCESS
    assert dag_run.state == success
