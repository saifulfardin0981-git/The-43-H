from pydantic import BaseModel
from datetime import datetime

class NoticeBase(BaseModel):
    title: str
    content: str
    resources_link: str | None = None

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    resources_link: str | None = None

class NoticeResponse(NoticeBase):
    id: int
    author_name: str
    created_at: datetime

    class Config:
        from_attributes = True
