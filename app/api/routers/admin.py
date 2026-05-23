from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_absolute_admin
from app.models.site_settings import SiteSettings
from app.models.user import User
from app.schemas.site_settings import SiteSettingsOut, SiteSettingsUpdate
from pydantic import BaseModel

router = APIRouter()

class UserAdUpdate(BaseModel):
    ads_enabled: bool

@router.get("/site-settings", response_model=SiteSettingsOut)
def get_site_settings(db: Session = Depends(get_db)):
    """Fetch global site settings"""
    settings = db.query(SiteSettings).first()
    if not settings:
        settings = SiteSettings(global_ads_enabled=True)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.patch("/site-settings", response_model=SiteSettingsOut)
def update_site_settings(
    settings_in: SiteSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_absolute_admin)
):
    """Update global site settings (Admin only)"""
    settings = db.query(SiteSettings).first()
    if not settings:
        settings = SiteSettings(global_ads_enabled=True)
        db.add(settings)
        db.commit()
    
    settings.global_ads_enabled = settings_in.global_ads_enabled
    db.commit()
    db.refresh(settings)
    return settings

@router.patch("/users/{user_id}/ads", response_model=UserAdUpdate)
def update_user_ads(
    user_id: int,
    ad_update: UserAdUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_absolute_admin)
):
    """Update ads_enabled for a specific user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.ads_enabled = ad_update.ads_enabled
    db.commit()
    db.refresh(user)
    return {"ads_enabled": user.ads_enabled}
