from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user, get_current_cr
from app.models.class_update import ClassUpdate
from app.models.user import User
from app.schemas.class_update import ClassUpdateCreate, ClassUpdateOut

router = APIRouter()

@router.get("/", response_model=List[ClassUpdateOut])
def read_class_updates(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve class updates. All authenticated users can view this.
    """
    updates = db.query(ClassUpdate).offset(skip).limit(limit).all()
    return updates

@router.post("/", response_model=ClassUpdateOut)
def create_class_update(
    *,
    db: Session = Depends(get_db),
    update_in: ClassUpdateCreate,
    current_user: User = Depends(get_current_cr),
) -> Any:
    """
    Create new class update. Only CRs (role >= 1) can post updates.
    """
    update = ClassUpdate(
        date=update_in.date,
        course_name=update_in.course_name,
        topics_covered=update_in.topics_covered,
        resources_link=update_in.resources_link,
        posted_by=current_user.id,
    )
    db.add(update)
    db.commit()
    db.refresh(update)
    return update
