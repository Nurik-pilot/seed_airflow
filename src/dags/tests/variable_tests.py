from airflow.models import Variable
from airflow.settings import Session


def test_variables() -> None:
    with (
        Session() as session,
        session.begin(),
    ):
        query = session.query(
            Variable,
        )
        assert query.count() == 0
