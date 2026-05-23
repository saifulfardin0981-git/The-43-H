from pydantic import BaseModel

class SiteSettingsBase(BaseModel):
    global_ads_enabled: bool

class SiteSettingsUpdate(BaseModel):
    global_ads_enabled: bool

class SiteSettingsOut(SiteSettingsBase):
    id: int

    class Config:
        from_attributes = True
