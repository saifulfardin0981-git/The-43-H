from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from app.core.config import settings
from app.api.routers import auth, class_updates, frontend, notices, academic, resources, semesters, admin, courses
from app.database import engine, Base
from app.models import User, ClassUpdate
from app.models.notice import Notice
from app.models.academic import Routine, Assignment, Resource, Semester, Course
from app.models.site_settings import SiteSettings
 # Ensure Notice model is imported for metadata

# Create database tables for boilerplate purposes
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url="/api/openapi.json"
)

# Handle Proxy Headers (Required for OAuth state validation behind HTTPS proxies)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Add SessionMiddleware (required for Authlib/OAuth)
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY_SESSION,
    same_site="lax",
    https_only=False  # Set to True if you want to force HTTPS-only cookies
)

# Include routers
app.include_router(frontend.router, tags=["frontend"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(class_updates.router, prefix="/api/class-updates", tags=["class updates"])
app.include_router(notices.router, prefix="/api/notices", tags=["notices"])
app.include_router(academic.router, prefix="/api/academic", tags=["academic"])
app.include_router(resources.router, prefix="/api/resources", tags=["resources"])
app.include_router(semesters.router, prefix="/api/semesters", tags=["semesters"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
