from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from app.database import Base

class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, index=True) # e.g., 'Monday'
    subject = Column(String)
    teacher = Column(String)
    time_slot = Column(String) # e.g., '10:00 AM - 11:30 AM'
    room_number = Column(String)

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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
