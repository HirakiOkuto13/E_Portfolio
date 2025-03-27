from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProfileCreate(BaseModel):
    full_name: str
    school: str
    grade: str
    bio: Optional[str] = None

class ActivityCreate(BaseModel):
    title: str
    description: str
    category: str
    date_started: datetime
    date_ended: Optional[datetime] = None
    image_url: Optional[str] = None

class AwardCreate(BaseModel):
    title: str
    description: str
    issuer: str
    date_received: datetime
    category: str
    level: str
    image_url: Optional[str] = None