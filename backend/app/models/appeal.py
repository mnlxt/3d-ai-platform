from sqlalchemy import Column, String, Text, JSON, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
from datetime import datetime


class Appeal(BaseModel):
    __tablename__ = "appeals"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(ENUM("account", "content", "other"), nullable=False, default="other")
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(ENUM("pending", "processing", "resolved", "rejected"), default="pending", nullable=False, index=True)
    admin_response = Column(Text, nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    attachments = Column(JSON, default=list)

    # 关联关系
    user = relationship("User", foreign_keys=[user_id], back_populates="appeals")
    resolver = relationship("User", foreign_keys=[resolved_by])
