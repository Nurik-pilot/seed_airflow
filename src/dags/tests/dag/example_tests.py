from datetime import datetime

from airflow import DAG
from airflow.models import (
    DagBag, DagRun,
)
from airflow.settings import Session
from pytest import mark
from sqlalchemy.orm import Query

from dags.tests.functions import (
    is_successful,
)


@mark.timeout(timeout=8)
def test_example_dag(
    dag_bag: DagBag,
) -> None:
    dag_id = 'example'
    dag: DAG
    dag = dag_bag.get_dag(
        dag_id=dag_id,
    )
    logical_date = datetime.fromisoformat(
        '2024-05-27T01:00:00+00:00',
    )
    query: Query
    with (
        Session() as session,
        session.begin(),
    ):
        query = session.query(
            DagRun,
        ).filter_by(
            dag_id=dag_id,
            execution_date=logical_date,
        )
        query.delete()
    dag_run: DagRun = dag.test(
        execution_date=logical_date,
    )
    assert is_successful(
        dag_run=dag_run,
    )
