from airflow.models import DagBag

expected_dag_ids = [
    'empty', 'example',
]


def test_no_import_errors(
    dag_bag: DagBag,
) -> None:
    assert len(
        dag_bag.import_errors,
    ) == 0


def test_dag_ids(
    dag_bag: DagBag,
) -> None:
    assert sorted(
        dag_bag.dag_ids,
    ) == sorted(
        expected_dag_ids,
    )


def test_dags_count(
    dag_bag: DagBag,
) -> None:
    assert dag_bag.size() == len(
        expected_dag_ids,
    )
