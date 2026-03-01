from sqlalchemy import Column, String, Boolean, Text, JSON
from sqlalchemy.dialects.mysql import ENUM
from app.db.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    gender = Column(ENUM("male", "female", "secret"), default="secret", nullable=False)
    bio = Column(Text, nullable=True)
    
    role = Column(ENUM("admin", "creator", "viewer"), default="viewer", nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    preferences = Column(JSON, default={
        "theme": "light",
        "language": "zh-CN",
        "auto_save": True,
        "default_model_format": "gltf"
    })
