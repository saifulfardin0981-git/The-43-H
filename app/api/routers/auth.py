import re
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from app.core import security
from app.core.config import settings
from app.core.dependencies import get_db, get_current_user, get_43h_student, get_absolute_admin
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserOut, UserRoleUpdate, UserUpdate

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

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@router.patch("/me", response_model=UserOut)
async def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile info"""
    if user_update.name is not None:
        current_user.name = user_update.name

    if user_update.blood_group is not None:
        valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"]
        if user_update.blood_group not in valid_groups:
            raise HTTPException(status_code=400, detail="Invalid blood group")
        current_user.blood_group = user_update.blood_group
    
    if user_update.phone is not None:
        current_user.phone = user_update.phone
        
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/users", response_model=list[UserOut])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_43h_student)
):
    """Get all 43-H users (Role >= 2)"""
    return db.query(User).filter(User.role >= 2).all()

@router.get("/admin/users", response_model=list[UserOut])
async def admin_get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_absolute_admin)
):
    """Admin: Get all users in the database"""
    return db.query(User).all()

@router.patch("/users/{user_email}/role", response_model=UserOut)
async def update_user_role(
    user_email: str,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_absolute_admin)
):
    """Admin: Update target user's role"""
    if role_update.role < 1 or role_update.role > 4:
        raise HTTPException(status_code=400, detail="Invalid role. Must be between 1 and 4.")
    
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user

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
    
    # Extract student ID (format: 242-35-213)
    id_pattern = r"\b\d{3}-\d{2}-\d{3}\b"
    id_match = re.search(id_pattern, email)
    
    raw_name = user_info.get('name', 'DIU Student')
    if not id_match:
        id_match = re.search(id_pattern, raw_name)
    
    student_id = id_match.group(0) if id_match else email.split('@')[0]
    
    # Clean and Format Name: remove student ID, strip, and Title Case
    clean_name = re.sub(id_pattern, "", raw_name).strip().title()
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Auto-create new user with role 1
        user = User(
            name=clean_name,
            email=email,
            student_id=student_id,
            phone="",
            role=1
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user info if it changed
        user.name = clean_name
        user.student_id = student_id
        db.commit()
    
    access_token = security.create_access_token(user.email)
    return RedirectResponse(url=f"/login?token={access_token}")
