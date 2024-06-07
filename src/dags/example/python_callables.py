from datetime import datetime

from airflow.models import Variable
from polars import DataFrame

from clients.s3_client import (
    S3Client,
)


def write_example_parquet(
    logical_date: datetime,
    **kwargs,
) -> dict[str, str | bool]:
    template: str = '/'.join(
        (
            'year=%Y', 'month=%m',
            'day=%d', 'date=%Y%m%d',
        ),
    )
    starts_at = logical_date.replace(
        minute=0, second=0,
        microsecond=0,
    )
    folder = 'files'
    partition = starts_at.strftime(
        format=template,
    )
    name = starts_at.isoformat()
    extension = 'parquet'
    filename: str = '.'.join(
        (
            name, extension,
        ),
    )
    key = '/'.join(
        (
            folder,
            partition,
            filename,
        ),
    )
    login = Variable.get(
        key='s3_login',
    )
    password = Variable.get(
        key='s3_password',
    )
    host = Variable.get(
        key='s3_host',
    )
    bucket = Variable.get(
        key='s3_bucket',
    )
    s3 = S3Client(
        login=login,
        password=password,
        host=host,
        bucket=bucket,
    )
    if s3.exists(key=key):
        return {
            'key': key,
            'exists': True,
        }
    numbers = tuple(range(100))
    sample = DataFrame(
        data={
            'integer': numbers,
        },
    )
    s3.write_dataframe(
        key=key, dataframe=sample,
    )
    return {
        'key': key,
        'exists': False,
    }
