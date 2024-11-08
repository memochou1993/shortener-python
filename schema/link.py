from pydantic import BaseModel, HttpUrl


class LinkCreateRequest(BaseModel):
    link: HttpUrl


class LinkCreateResponse(BaseModel):
    code: str
