from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    student_id = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(Integer, default=1) # 1: DIU Student, 2: 43-H Student, 3: CR, 4: Absolute Admin
    blood_group = Column(String, nullable=True)

    # Establish relationship with ClassUpdate
    class_updates = relationship("ClassUpdate", back_populates="author")
