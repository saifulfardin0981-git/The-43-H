from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"request": request})

@router.get("/directory", response_class=HTMLResponse)
async def directory_page(request: Request):
    return templates.TemplateResponse(request=request, name="directory.html", context={"request": request})

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse(request=request, name="profile.html", context={"request": request})

@router.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    return templates.TemplateResponse(request=request, name="resources.html", context={"request": request})
