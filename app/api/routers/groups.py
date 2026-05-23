from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, get_current_cr
from app.models.academic import GroupLink, Semester
from app.models.user import User
from app.schemas.academic import GroupLinkCreate, GroupLinkResponse

router = APIRouter()

@router.get("/", response_model=List[GroupLinkResponse])
def get_group_links(
    semester_id: Optional[int] = Query(None, description="Filter by semester ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all group links for a semester"""
    query = db.query(GroupLink)
    if semester_id:
        query = query.filter(GroupLink.semester_id == semester_id)
    else:
        # Default to current semester
        current_sem = db.query(Semester).filter(Semester.is_current == True).first()
        if current_sem:
            query = query.filter(GroupLink.semester_id == current_sem.id)
    
    return query.all()

@router.post("/", response_model=GroupLinkResponse)
def create_group_link(
    link_in: GroupLinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Create a new group link (CR/Admin only)"""
    new_link = GroupLink(**link_in.model_dump())
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Delete a group link (CR/Admin only)"""
    link = db.query(GroupLink).filter(GroupLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Group link not found")
    
    db.delete(link)
    db.commit()
    return None
