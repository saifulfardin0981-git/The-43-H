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
    
    courses = relationship("Course", back_populates="semester")
    resources = relationship("Resource", back_populates="semester")
    group_links = relationship("GroupLink", back_populates="semester")

class GroupLink(Base):
    __tablename__ = "group_links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    link = Column(String)
    semester_id = Column(Integer, ForeignKey("semesters.id"))

    semester = relationship("Semester", back_populates="group_links")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True) # e.g., 'SWE112'
    name = Column(String) # e.g., 'Software Engineering'
    semester_id = Column(Integer, ForeignKey("semesters.id"))

    semester = relationship("Semester", back_populates="courses")
    resources = relationship("Resource", back_populates="course")

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
    link = Column(String)
    category = Column(String, default='Other') # e.g., 'Shared Link', 'BLC Link', 'Notes', 'Other'
    author_name = Column(String)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    semester = relationship("Semester", back_populates="resources")
    course = relationship("Course", back_populates="resources")
