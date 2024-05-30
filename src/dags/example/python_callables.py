from datetime import datetime

from airflow.models import Variable
from polars import DataFrame
from pyarrow.fs import S3FileSystem


def write_example_parquet(
    logical_date: datetime,
    **kwargs,
) -> str:
    numbers = tuple(range(10000))
    sample = DataFrame(
        data={
            'integer': numbers,
        },
    )
    template: str = '/'.join(
        (
            'year=%Y',
            'month=%m',
            'day=%d',
            'date=%Y%m%d',
        ),
    )
    starts_at = logical_date.replace(
        minute=0, second=0,
        microsecond=0,
    )
    partition = starts_at.strftime(
        format=template,
    )
    filename = '.'.join(
        (
            starts_at.isoformat(),
            'parquet',
        ),
    )
    destination = '/'.join(
        (
            'seed', 'files',
            partition, filename,
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
    filesystem = S3FileSystem(
        access_key=login,
        secret_key=password,
        endpoint_override=host,
    )
    with filesystem.open_output_stream(
        path=destination,
    ) as stream:
        sample.write_parquet(
            file=stream,
            use_pyarrow=True,
        )
    return destination
