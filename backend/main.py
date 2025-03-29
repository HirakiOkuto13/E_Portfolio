from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
import models
from database import SessionLocal
from dotenv import load_dotenv
import os
from pydantic import BaseModel, EmailStr
import schemas

load_dotenv()  # load environment variables from .env file

# API Settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI(title="E-Portfolio API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication Functions
def get_password_hash(password: str) -> bytes:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password=hashed_password)

def create_access_token(data: dict):
    """
    Create a JWT access token with expiration time in UTC+7 timezone

    """
    to_encode = data.copy()
    bangkok_tz = timezone(timedelta(hours=7))
    expire = datetime.now(bangkok_tz) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Authentication Endpoints
@app.post("/token", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"email": db_user.email, "role": db_user.role}

# Profile Endpoints
@app.post("/profile", status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: schemas.StudentProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    db_profile = models.StudentProfile(
        **profile.dict(),
        user_id=current_user.id
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.get("/profile")
async def get_profile(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# Base endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to E-Portfolio API"}

# Activity endpoints
@app.post("/activities")
async def create_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db_activity = models.Activity(**activity.dict(), student_id=profile.id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@app.get("/activities")
async def get_activities(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return db.query(models.Activity).filter(models.Activity.student_id == profile.id).all()

# Award endpoints
@app.post("/awards")
async def create_award(
    award: schemas.AwardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db_award = models.Award(**award.dict(), student_id=profile.id)
    db.add(db_award)
    db.commit()
    db.refresh(db_award)
    return db_award

@app.get("/awards")
async def get_awards(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return db.query(models.Award).filter(models.Award.student_id == profile.id).all()

# Portfolio view endpoint
@app.get("/portfolio/{user_id}")
async def get_portfolio(user_id: int, db: Session = Depends(get_db)):
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