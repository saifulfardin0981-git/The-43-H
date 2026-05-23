from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoutineBase(BaseModel):
    day_of_week: str
    subject: str
    teacher: str
    time_slot: str
    room_number: str

class RoutineCreate(RoutineBase):
    pass

class RoutineUpdate(BaseModel):
    day_of_week: Optional[str] = None
    subject: Optional[str] = None
    teacher: Optional[str] = None
    time_slot: Optional[str] = None
    room_number: Optional[str] = None

class RoutineResponse(RoutineBase):
    id: int

    class Config:
        from_attributes = True

class AssignmentBase(BaseModel):
    title: str
    subject: str
    due_date: datetime
    description: Optional[str] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    due_date: Optional[datetime] = None
    description: Optional[str] = None

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        from_attributes = True

class ResourceBase(BaseModel):
    title: str
    subject: str
    link: str

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: int
    author_name: str
    created_at: datetime

    class Config:
        from_attributes = True
