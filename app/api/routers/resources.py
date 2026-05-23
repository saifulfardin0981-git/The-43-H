from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user, get_current_cr
from app.models.academic import Resource
from app.models.user import User
from app.schemas.academic import ResourceCreate, ResourceResponse

router = APIRouter()

@router.get("/", response_model=List[ResourceResponse])
def get_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all academic resources (Role >= 1)"""
    return db.query(Resource).order_by(Resource.created_at.desc()).all()

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
        author_name=current_user.name
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
