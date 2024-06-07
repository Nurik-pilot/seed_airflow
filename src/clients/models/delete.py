from pydantic import BaseModel, Field

from .shared import ResponseMetadata


class DeleteResponse(BaseModel):
    response_metadata: ResponseMetadata = Field(
        alias='ResponseMetadata',
    )
