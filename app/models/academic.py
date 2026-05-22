from sqlalchemy import Column, Integer, String, Text, DateTime
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
