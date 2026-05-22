from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.dependencies import get_current_user, get_current_cr
from app.models.academic import Routine, Assignment
from app.models.user import User
from app.schemas.academic import (
    RoutineCreate, RoutineResponse,
    AssignmentCreate, AssignmentResponse
)

router = APIRouter()

# --- Routine Endpoints ---

@router.get("/routines", response_model=List[RoutineResponse])
def get_routines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all class routines"""
    return db.query(Routine).all()

@router.post("/routines", response_model=RoutineResponse)
def create_routine(
    routine_in: RoutineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Create a new routine entry (CR/Admin only)"""
    new_routine = Routine(**routine_in.model_dump())
    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)
    return new_routine

@router.delete("/routines/{routine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Delete a routine entry (CR/Admin only)"""
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    db.delete(routine)
    db.commit()
    return None

# --- Assignment Endpoints ---

@router.get("/assignments", response_model=List[AssignmentResponse])
def get_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all upcoming assignments"""
    return db.query(Assignment).order_by(Assignment.due_date.asc()).all()

@router.post("/assignments", response_model=AssignmentResponse)
def create_assignment(
    assignment_in: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Create a new assignment (CR/Admin only)"""
    new_assignment = Assignment(**assignment_in.model_dump())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Delete an assignment (CR/Admin only)"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return None
