from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from models import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.STUDENT

class StudentProfileCreate(BaseModel):
    first_name: str
    last_name: str
    student_id: str
    grade: Optional[int] = None
    school: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class StudentProfileBase(BaseModel):
    first_name: str
    last_name: str
    student_id: str
    grade: Optional[int] = None
    school: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    hours: Optional[int] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AwardBase(BaseModel):
    title: str
    description: Optional[str] = None
    award_type: Optional[str] = None
    issuer: Optional[str] = None
    date_received: Optional[datetime] = None
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class StudentSkillBase(BaseModel):
    skill_id: int
    proficiency_level: int
    model_config = ConfigDict(from_attributes=True)

# Create Schemas
class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.STUDENT

class StudentProfileCreate(StudentProfileBase):
    pass

class ActivityCreate(ActivityBase):
    pass

class AwardCreate(AwardBase):
    pass

class SkillCreate(SkillBase):
    pass

class StudentSkillCreate(StudentSkillBase):
    pass

# Response Schemas
class Skill(SkillBase):
    id: int
    created_at: datetime

class StudentSkill(StudentSkillBase):
    id: int
    created_at: datetime
    updated_at: datetime
    skill: Skill

class Award(AwardBase):
    id: int
    student_id: int
    created_at: datetime
    updated_at: datetime

class Activity(ActivityBase):
    id: int
    student_id: int
    created_at: datetime
    updated_at: datetime

class StudentProfile(StudentProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    activities: List[Activity] = []
    awards: List[Award] = []
    skills: List[StudentSkill] = []

class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime
    profile: Optional[StudentProfile] = None

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)