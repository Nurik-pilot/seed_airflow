from pydantic import BaseModel, Field

from .shared import ResponseMetadata


class ListV2Response(BaseModel):
    response_metadata: ResponseMetadata = Field(
        alias='ResponseMetadata',
    )
    is_truncated: bool = Field(
        alias='IsTruncated',
    )
    name: str = Field(alias='Name')
    prefix: str = Field(
        alias='Prefix',
    )
    max_keys: int = Field(
        alias='MaxKeys',
    )
    encoding_type: str = Field(
        alias='EncodingType',
    )
    key_count: int = Field(
        alias='KeyCount',
    )
