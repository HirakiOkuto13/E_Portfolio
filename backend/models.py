from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(LargeBinary)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="user")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String(100))
    school = Column(String(100))
    grade = Column(String(20))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    user = relationship("User", back_populates="profile")
    activities = relationship("Activity", back_populates="student")
    awards = relationship("Award", back_populates="student")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    title = Column(String(200))
    description = Column(Text)
    category = Column(String(50))  # e.g., Academic, Sports, Arts, Leadership
    date_started = Column(DateTime)
    date_ended = Column(DateTime, nullable=True)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    student = relationship("StudentProfile", back_populates="activities")

class Award(Base):
    __tablename__ = "awards"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    title = Column(String(200))
    description = Column(Text)
    issuer = Column(String(100))
    date_received = Column(DateTime)
    category = Column(String(50))  # e.g., Academic, Sports, Competition
    level = Column(String(50))  # e.g., School, District, National
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    student = relationship("StudentProfile", back_populates="awards")