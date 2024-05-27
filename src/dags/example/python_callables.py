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
    destination = '/'.join(
        (
            'seed', 'files',
            'example.parquet',
        ),
    )
    filesystem = S3FileSystem(
        access_key=Variable.get(
            key='s3_login',
        ),
        secret_key=Variable.get(
            key='s3_password',
        ),
        endpoint_override=Variable.get(
            key='s3_host',
        ),
    )
    with filesystem.open_output_stream(
        path=destination,
    ) as stream:
        sample.write_parquet(
            file=stream,
            use_pyarrow=True,
        )
    return destination
