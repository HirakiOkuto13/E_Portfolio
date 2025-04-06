from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
import app.models.models as models
import app.schemas.schemas as schemas

router = APIRouter()

@router.get("/portfolio/{user_id}")
async def get_portfolio(user_id: int, db: Session = Depends(deps.get_db)):
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    activities = db.query(models.Activity).filter(models.Activity.student_id == profile.id).all()
    awards = db.query(models.Award).filter(models.Award.student_id == profile.id).all()
    
    return {
        "profile": profile,
        "activities": activities,
        "awards": awards
    }