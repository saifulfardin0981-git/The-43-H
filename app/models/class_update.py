from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ClassUpdate(Base):
    __tablename__ = "class_updates"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    course_name = Column(String, index=True)
    topics_covered = Column(String)
    resources_link = Column(String, nullable=True)
    posted_by = Column(Integer, ForeignKey("users.id"))

    # Establish relationship with User
    author = relationship("User", back_populates="class_updates")
