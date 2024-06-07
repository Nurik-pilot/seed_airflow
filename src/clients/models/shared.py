from pydantic import (
    BaseModel, Field,
)


class HTTPHeaders(BaseModel):
    accept_ranges: str = Field(
        alias='accept-ranges',
    )
    server: str = Field(
        alias='server',
    )
    strict_transport_security: str = Field(
        alias='strict-transport-security',
    )
    vary: str = Field(alias='vary')
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
    date: str = Field(alias='date')


class ResponseMetadata(BaseModel):
    request_id: str = Field(
        alias='RequestId',
    )
    host_id: str = Field(
        alias='HostId',
    )
    http_status_code: int = Field(
        alias='HTTPStatusCode',
    )
    http_headers: HTTPHeaders = Field(
        alias='HTTPHeaders',
    )
    retry_attempts: int = Field(
        alias='RetryAttempts',
    )
