from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from app.core import security
from app.core.config import settings
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.token import Token

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))

@router.get("/callback", name="auth_callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate with Google")
    
    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to get user info from Google")
    
    email = user_info.get('email')
    if not email or not email.endswith("@diu.edu.bd"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access restricted to DIU email addresses (@diu.edu.bd)"
        )
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Auto-create new user with role 1
        user = User(
            name=user_info.get('name', 'DIU Student'),
            email=email,
            student_id=email.split('@')[0], # Fallback student_id from email
            phone="",
            role=1 # Any DIU Student
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    access_token = security.create_access_token(user.email)
    
    # Redirect to frontend login page with token so JS can store it
    return RedirectResponse(url=f"/login?token={access_token}")
