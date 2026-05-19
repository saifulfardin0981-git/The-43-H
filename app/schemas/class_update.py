from pydantic import BaseModel
from datetime import date
from typing import Optional

class ClassUpdateBase(BaseModel):
    date: date
    course_name: str
    topics_covered: str
    resources_link: Optional[str] = None

class ClassUpdateCreate(ClassUpdateBase):
    pass

class ClassUpdateOut(ClassUpdateBase):
    id: int
    posted_by: int

    class Config:
        from_attributes = True
