from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoutineBase(BaseModel):
    day_of_week: str
    course_code: Optional[str] = None
    subject: str
    teacher: str
    time_slot: str
    room_number: str
    group: str = 'Combined'

class RoutineCreate(RoutineBase):
    pass

class RoutineUpdate(BaseModel):
    day_of_week: Optional[str] = None
    course_code: Optional[str] = None
    subject: Optional[str] = None
    teacher: Optional[str] = None
    time_slot: Optional[str] = None
    room_number: Optional[str] = None
    group: Optional[str] = None

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

class SemesterBase(BaseModel):
    code: str
    name: str
    is_current: bool = False

class SemesterCreate(SemesterBase):
    pass

class SemesterResponse(SemesterBase):
    id: int

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    code: str
    name: str
    semester_id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    semester_id: Optional[int] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True

class ResourceBase(BaseModel):
    title: str
    link: str
    category: str
    semester_id: int
    course_id: int

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    category: Optional[str] = None
    semester_id: Optional[int] = None
    course_id: Optional[int] = None

class ResourceResponse(ResourceBase):
    id: int
    author_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class GroupLinkBase(BaseModel):
    title: str
    link: str
    semester_id: int

class GroupLinkCreate(GroupLinkBase):
    pass

class GroupLinkResponse(GroupLinkBase):
    id: int

    class Config:
        from_attributes = True
