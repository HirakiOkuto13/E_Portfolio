from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone, timedelta
import enum

class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

def get_utc_now():
    """
    Returns current UTC+7 (Bangkok/Jakarta) time as timezone-aware datetime
    """
    bangkok_tz = timezone(timedelta(hours=7))
    return datetime.now(bangkok_tz)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    profile = relationship("StudentProfile", back_populates="user", uselist=False)

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    student_id = Column(String(20), unique=True)
    grade = Column(Integer)
    school = Column(String(255))
    bio = Column(Text)
    avatar_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    user = relationship("User", back_populates="profile")
    activities = relationship("Activity", back_populates="student")
    awards = relationship("Award", back_populates="student")
    skills = relationship("StudentSkill", back_populates="student")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    activity_type = Column(String(100))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    hours = Column(Integer)
    location = Column(String(255))
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    student = relationship("StudentProfile", back_populates="activities")

class Award(Base):
    __tablename__ = "awards"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    award_type = Column(String(100))
    issuer = Column(String(255))
    date_received = Column(DateTime(timezone=True))
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    student = relationship("StudentProfile", back_populates="awards")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    proficiency_level = Column(Integer)  # 1-5
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    student = relationship("StudentProfile", back_populates="skills")
    skill = relationship("Skill")