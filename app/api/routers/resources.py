from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, get_current_cr
from app.models.academic import Resource, Semester
from app.models.user import User
from app.schemas.academic import ResourceCreate, ResourceResponse

router = APIRouter()

@router.get("/", response_model=List[ResourceResponse])
def get_resources(
    semester_code: Optional[str] = Query(None, description="Semester code to filter by"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch academic resources (Role >= 1), optionally filtered by semester"""
    query = db.query(Resource)
    
    if semester_code:
        semester = db.query(Semester).filter(Semester.code == semester_code).first()
        if not semester:
            return [] # No resources for a non-existent semester
        query = query.filter(Resource.semester_id == semester.id)
    else:
        # Default to current semester
        current_sem = db.query(Semester).filter(Semester.is_current == True).first()
        if current_sem:
            query = query.filter(Resource.semester_id == current_sem.id)

    return query.order_by(Resource.created_at.desc()).all()

@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource_in: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Create a new academic resource (Role >= 3)"""
    new_resource = Resource(
        title=resource_in.title,
        subject=resource_in.subject,
        link=resource_in.link,
        author_name=current_user.name,
        semester_id=resource_in.semester_id
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_cr)
):
    """Delete an academic resource (Role >= 3)"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(resource)
    db.commit()
    return None
