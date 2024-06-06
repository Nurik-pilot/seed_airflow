from boto3 import client
from pydantic import BaseModel, Field


class HTTPHeaders(BaseModel):
    accept_ranges: str = Field(
        alias='accept-ranges',
    )
    server: str
    strict_transport_security: str = Field(
        alias='strict-transport-security',
    )
    vary: str
    x_amz_id_2: str = Field(
        alias='x-amz-id-2',
    )
    x_amz_request_id: str = Field(
        alias='x-amz-request-id',
    )
    x_content_type_options: str = Field(
        alias='x-content-type-options',
    )
    x_xss_protection: str = Field(
        alias='x-xss-protection',
    )
    date: str


class ResponseMetadata(BaseModel):
    request_id: str = Field(alias='RequestId')
    host_id: str = Field(alias='HostId')
    http_status_code: int = Field(alias='HTTPStatusCode')
    http_headers: HTTPHeaders = Field(alias='HTTPHeaders')
    retry_attempts: int = Field(alias='RetryAttempts')


class DeleteResponse(BaseModel):
    response_meta_data: ResponseMetadata = Field(
        alias='ResponseMetadata',
    )


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
