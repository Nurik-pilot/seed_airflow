from airflow.models import (
    Connection,
)
from airflow.settings import (
    Session,
)
from sqlalchemy.orm import Query

from setup import (
    setup_s3_connection,
)


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
    with (
        Session() as session,
        session.begin(),
    ):
        query = session.query(
            Connection,
        )
        assert query.count() == 1
