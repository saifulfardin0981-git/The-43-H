from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    student_id: str
    phone: str
    role: int = 1
    blood_group: str | None = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    blood_group: str | None = None
    phone: str | None = None

class UserOut(UserBase):
    id: int
    ads_enabled: bool

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: int
