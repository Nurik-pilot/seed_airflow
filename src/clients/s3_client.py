from boto3 import client
from polars import DataFrame
from pyarrow.fs import (
    S3FileSystem,
)

from .models import (
    DeleteResponse,
    ListV2Response,
)


class S3Client:
    __login: str
    __password: str
    __host: str
    __bucket: str

    def __init__(
        self,
        login: str,
        password: str,
        host: str,
        bucket: str,
    ) -> None:
        super().__init__()
        self.__login = login
        self.__password = password
        self.__host = host
        self.__bucket = bucket
        self.__s3 = client(
            service_name='s3',
            aws_access_key_id=login,
            aws_secret_access_key=password,
            endpoint_url=host,
        )

    def exists(
        self, key: str,
    ) -> bool:
        raw = self.__s3.list_objects_v2(
            Bucket=self.__bucket,
            Prefix=key, MaxKeys=1,
        )
        validated = ListV2Response.model_validate(
            obj=raw,
        )
        return validated.key_count >= 1

    def delete(
        self, key: str,
    ) -> DeleteResponse:
        raw = self.__s3.delete_object(
            Bucket=self.__bucket, Key=key,
        )
        return DeleteResponse.model_validate(
            obj=raw,
        )

    def write_dataframe(
        self, key: str,
        dataframe: DataFrame,
    ) -> None:
        filesystem = S3FileSystem(
            access_key=self.__login,
            secret_key=self.__password,
            endpoint_override=self.__host,
        )
        destination = '/'.join(
            (self.__bucket, key,),
        )
        with filesystem.open_output_stream(
            path=destination,
        ) as stream:
            dataframe.write_parquet(
                file=stream,
                use_pyarrow=True,
            )
