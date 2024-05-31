from datetime import datetime
from typing import Any

from airflow import DAG
from airflow.models import DagRun, XCom
from airflow.settings import Session
from airflow.utils.state import (
    DagRunState,
)
from sqlalchemy.orm import Query


def is_successful(
    dag_run: DagRun,
) -> bool:
    success = DagRunState.SUCCESS
    return dag_run.state == success


def clear_dag_run(
    dag: DAG,
    logical_date: datetime,
) -> None:
    query: Query
    with (
        Session() as session,
        session.begin(),
    ):
        query = session.query(
            DagRun,
        ).filter_by(
            dag_id=dag.dag_id,
            execution_date=logical_date,
        )
        query.delete()


def obtain_return_value(
    dag: DAG, task_id: str,
    dag_run: DagRun,
) -> Any:
    with (
        Session() as session,
        session.begin(),
    ):
        result = session.query(
            XCom,
        ).filter_by(
            dag_id=dag.dag_id,
            task_id=task_id,
            dag_run_id=dag_run.id,
        ).limit(limit=1).one()
    return result.value
