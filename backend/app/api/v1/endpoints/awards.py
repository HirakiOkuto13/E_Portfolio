from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
import app.models.models as models
import app.schemas.schemas as schemas

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_award(
    award: schemas.AwardCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db_award = models.Award(**award.dict(), student_id=profile.id)
    db.add(db_award)
    db.commit()
    db.refresh(db_award)
    return db_award

@router.get("/")
async def get_awards(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return db.query(models.Award).filter(models.Award.student_id == profile.id).all()