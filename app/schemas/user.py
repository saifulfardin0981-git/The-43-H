from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    student_id: str
    phone: str
    role: int = 1

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: int
