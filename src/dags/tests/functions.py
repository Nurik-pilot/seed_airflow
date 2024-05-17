from airflow.models import DagRun
from airflow.utils.state import (
    DagRunState,
)


def is_successful(
    dag_run: DagRun,
) -> bool:
    success = DagRunState.SUCCESS
    return dag_run.state == success
