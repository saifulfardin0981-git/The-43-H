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

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        from_attributes = True
