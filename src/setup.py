from contextlib import suppress
from json import dumps

from airflow.models import (
    Connection, Variable,
)
from airflow.settings import Session
from sqlalchemy.exc import (
    IntegrityError,
)


def setup_s3_connection() -> None:
    conn_id: str = Variable.get(
        key='s3_conn_id',
    )
    conn_type: str = Variable.get(
        key='s3_conn_type',
    )
    login: str = Variable.get(
        key='s3_login',
    )
    password: str = Variable.get(
        key='s3_password',
    )
    host: str = Variable.get(
        key='s3_host',
    )
    region: str = Variable.get(
        key='s3_region',
    )
    obj: dict[str, str] = {
        'aws_access_key_id': login,
        'aws_secret_access_key': password,
        'endpoint_url': host,
        'region_name': region,
    }
    extra: str = dumps(obj=obj)
    connection: Connection = Connection(
        conn_id=conn_id,
        conn_type=conn_type,
        login=login,
        password=password,
        extra=extra,
    )
    with (
        suppress(IntegrityError),
        Session() as session,
        session.begin(),
    ):
        session.add(instance=connection)


if __name__ == '__main__':
    setup_s3_connection()
