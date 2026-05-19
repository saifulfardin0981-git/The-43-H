from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.api.routers import auth, class_updates, frontend
from app.database import engine, Base
from app.models import User, ClassUpdate

# Create database tables for boilerplate purposes
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url="/api/openapi.json"
)

# Add SessionMiddleware (required for Authlib/OAuth)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY_SESSION)

# Include routers
app.include_router(frontend.router, tags=["frontend"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(class_updates.router, prefix="/api/class-updates", tags=["class updates"])
