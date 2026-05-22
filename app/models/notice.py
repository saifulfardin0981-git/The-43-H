from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_name = Column(String)
    resources_link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
