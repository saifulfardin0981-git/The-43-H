from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import SessionLocal
from app.models.user import User
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# 4-level role architecture: 1: DIU Student, 2: 43-H Student, 3: CR, 4: Absolute Admin

def get_43h_student(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role < 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to 43-H Students or higher"
        )
    return current_user

def get_current_cr(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to CRs or higher"
        )
    return current_user

def get_absolute_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role < 4:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to Absolute Admins"
        )
    return current_user
