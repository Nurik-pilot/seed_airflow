from datetime import datetime

from airflow.models import Variable
from polars import DataFrame
from pyarrow.fs import S3FileSystem

from clients.s3_client import S3Client


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
    bucket = 'seed'
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
    s3 = S3Client(
        login=login,
        password=password,
        host=host,
    )
    if s3.exists(
        bucket=bucket, key=key,
    ):
        return {
            'bucket': bucket,
            'key': key,
            'exists': True,
        }
    numbers = tuple(range(100))
    sample = DataFrame(
        data={
            'integer': numbers,
        },
    )
    filesystem = S3FileSystem(
        access_key=login,
        secret_key=password,
        endpoint_override=host,
    )
    destination = '/'.join(
        (bucket, key,),
    )
    with filesystem.open_output_stream(
        path=destination,
    ) as stream:
        sample.write_parquet(
            file=stream,
            use_pyarrow=True,
        )
    return {
        'bucket': bucket,
        'key': key,
        'exists': False,
    }
