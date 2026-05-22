from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user, get_current_cr
from app.models.notice import Notice
from app.models.user import User
from app.schemas.notice import NoticeCreate, NoticeResponse

router = APIRouter()

@router.get("/", response_model=List[NoticeResponse])
def get_notices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all notices ordered by newest first"""
    return db.query(Notice).order_by(Notice.created_at.desc()).all()

@router.post("/", response_model=NoticeResponse)
def create_notice(
    notice_in: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Create a new notice (CR/Admin only)"""
    new_notice = Notice(
        title=notice_in.title,
        content=notice_in.content,
        author_name=current_user.name
    )
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice

@router.delete("/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Delete a notice (CR/Admin only)"""
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    db.delete(notice)
    db.commit()
    return None
