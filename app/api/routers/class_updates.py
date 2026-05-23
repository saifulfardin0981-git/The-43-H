from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user, get_current_cr
from app.models.class_update import ClassUpdate
from app.models.user import User
from app.schemas.class_update import ClassUpdateCreate, ClassUpdateUpdate, ClassUpdateOut

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
    updates = db.query(ClassUpdate).order_by(ClassUpdate.date.desc()).offset(skip).limit(limit).all()
    return updates

@router.post("/", response_model=ClassUpdateOut)
def create_class_update(
    *,
    db: Session = Depends(get_db),
    update_in: ClassUpdateCreate,
    current_user: User = Depends(get_current_cr),
) -> Any:
    """
    Create new class update. Only CRs (role >= 3) can post updates.
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

@router.patch("/{update_id}", response_model=ClassUpdateOut)
def update_class_update(
    *,
    db: Session = Depends(get_db),
    update_id: int,
    update_in: ClassUpdateUpdate,
    current_user: User = Depends(get_current_cr),
) -> Any:
    """
    Update a class update. (CR/Admin only)
    """
    update = db.query(ClassUpdate).filter(ClassUpdate.id == update_id).first()
    if not update:
        raise HTTPException(status_code=404, detail="Update not found")
    
    update_data = update_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(update, key, value)
    
    db.commit()
    db.refresh(update)
    return update

@router.delete("/{update_id}")
def delete_class_update(
    *,
    db: Session = Depends(get_db),
    update_id: int,
    current_user: User = Depends(get_current_cr),
) -> Any:
    """
    Delete a class update. (CR/Admin only)
    """
    update = db.query(ClassUpdate).filter(ClassUpdate.id == update_id).first()
    if not update:
        raise HTTPException(status_code=404, detail="Update not found")
    db.delete(update)
    db.commit()
    return {"message": "Update deleted successfully"}
