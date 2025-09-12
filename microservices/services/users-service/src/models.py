from sqlalchemy import Column, String, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)


class UserProfile(BaseModel):
    __tablename__ = "user_profiles"

    user_id = Column(
        UUID(as_uuid=True), nullable=False
    )  # No foreign key for microservices
    years_experience = Column(Integer)
    skills = Column(JSON)  # JSON field for flexible skills storage
    career_goals = Column(Text)
    preferred_work_style = Column(String(50))  # remote, hybrid, onsite
