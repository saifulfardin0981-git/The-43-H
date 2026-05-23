from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.site_settings import SiteSettings

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_global_ads_enabled(db: Session):
    settings = db.query(SiteSettings).first()
    if settings:
        return settings.global_ads_enabled
    return True

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "global_ads_enabled": global_ads})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "global_ads_enabled": global_ads})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"request": request, "global_ads_enabled": global_ads})

@router.get("/directory", response_class=HTMLResponse)
async def directory_page(request: Request, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="directory.html", context={"request": request, "global_ads_enabled": global_ads})

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="profile.html", context={"request": request, "global_ads_enabled": global_ads})

@router.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="resources.html", context={"request": request, "global_ads_enabled": global_ads})

@router.get("/course/{course_id}", response_class=HTMLResponse)
async def course_detail_page(request: Request, course_id: int, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="course_detail.html", context={"request": request, "course_id": course_id, "global_ads_enabled": global_ads})

@router.get("/groups", response_class=HTMLResponse)
async def groups_page(request: Request, db: Session = Depends(get_db)):
    global_ads = get_global_ads_enabled(db)
    return templates.TemplateResponse(request=request, name="groups.html", context={"request": request, "global_ads_enabled": global_ads})
