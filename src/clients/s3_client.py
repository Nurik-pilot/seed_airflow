from boto3 import client

from .models import DeleteResponse


class S3Client:

    def __init__(
        self, login: str,
        password: str, host: str,
    ) -> None:
        super().__init__()
        self.s3 = client(
            service_name='s3',
            aws_access_key_id=login,
            aws_secret_access_key=password,
            endpoint_url=host,
        )

    def exists(
        self, bucket: str, key: str,
    ) -> bool:
        response: dict[str, int]
        response = self.s3.list_objects_v2(
            Bucket=bucket,
            Prefix=key, MaxKeys=1,
        )
        return response.get(
            'KeyCount', 0,
        ) >= 1

    def delete(
        self, bucket: str, key: str,
    ) -> DeleteResponse:
        response = self.s3.delete_object(
            Bucket=bucket, Key=key,
        )
        return DeleteResponse.model_validate(
            obj=response,
        )
