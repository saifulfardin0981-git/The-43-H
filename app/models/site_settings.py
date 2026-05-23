from sqlalchemy import Column, Integer, Boolean
from app.database import Base

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    global_ads_enabled = Column(Boolean, default=True)
