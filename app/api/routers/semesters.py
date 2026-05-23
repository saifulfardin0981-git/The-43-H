from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user, get_absolute_admin
from app.models.academic import Semester
from app.models.user import User
from app.schemas.academic import SemesterCreate, SemesterResponse

router = APIRouter()

@router.get("/", response_model=List[SemesterResponse])
def get_semesters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all semesters"""
    return db.query(Semester).order_by(Semester.code.desc()).all()

@router.get("/current", response_model=SemesterResponse)
def get_current_semester(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch the active semester"""
    semester = db.query(Semester).filter(Semester.is_current == True).first()
    if not semester:
        raise HTTPException(status_code=404, detail="No current semester set")
    return semester

@router.post("/", response_model=SemesterResponse)
def create_semester(
    semester_in: SemesterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_absolute_admin)
):
    """Create a new semester (Admin only)"""
    if semester_in.is_current:
        # Unset others
        db.query(Semester).update({Semester.is_current: False})
        
    new_semester = Semester(**semester_in.model_dump())
    db.add(new_semester)
    db.commit()
    db.refresh(new_semester)
    return new_semester

@router.delete("/{semester_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_semester(
    semester_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_absolute_admin)
):
    """Delete a semester (Admin only)"""
    semester = db.query(Semester).filter(Semester.id == semester_id).first()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    
    db.delete(semester)
    db.commit()
    return None
