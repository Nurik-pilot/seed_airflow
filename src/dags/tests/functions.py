from datetime import datetime
from typing import Any

from airflow import DAG
from airflow.models import (
    DagRun, XCom,
)
from airflow.settings import (
    Session,
)
from airflow.utils.state import (
    DagRunState,
)
from sqlalchemy.orm import (
    Query, )


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
    dag: DAG,
    task_id: str,
    dag_run: DagRun,
) -> Any:
    instance: XCom
    with (
        Session() as session,
        session.begin(),
    ):
        x_coms = session.query(
            XCom,
        )
        filtered = x_coms.filter_by(
            dag_id=dag.dag_id,
            task_id=task_id,
            dag_run_id=dag_run.id,
            key='return_value',
        )
        limited = filtered.limit(
            limit=1,
        )
        instance = limited.one()
    return instance.value
