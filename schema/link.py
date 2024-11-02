from pydantic import BaseModel


class LinkCreateRequest(BaseModel):
    link: str


class LinkCreateResponse(BaseModel):
    code: str
