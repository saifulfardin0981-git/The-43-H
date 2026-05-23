from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Semester(Base):
    __tablename__ = "semesters"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True) # e.g., '262'
    name = Column(String) # e.g., 'Summer 2026'
    is_current = Column(Boolean, default=False)
    
    resources = relationship("Resource", back_populates="semester")

class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, index=True) # e.g., 'Monday'
    course_code = Column(String, nullable=True) # e.g., 'SWE 331'
    subject = Column(String)
    teacher = Column(String)
    time_slot = Column(String) # e.g., '10:00 AM - 11:30 AM'
    room_number = Column(String)
    group = Column(String, nullable=True, default='Combined') # e.g., 'Combined', 'H1', 'H2'

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    subject = Column(String)
    due_date = Column(DateTime)
    description = Column(Text, nullable=True)

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    subject = Column(String, index=True)
    link = Column(String)
    author_name = Column(String)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    semester = relationship("Semester", back_populates="resources")
