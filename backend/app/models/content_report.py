from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
from datetime import datetime


class ContentReport(BaseModel):
    __tablename__ = "content_reports"

    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    reason = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(ENUM("pending", "reviewed", "dismissed"), default="pending", nullable=False, index=True)
    admin_notes = Column(Text, nullable=True)
    action_taken = Column(ENUM("none", "warning", "removed", "banned"), default="none", nullable=False)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    # 关联关系
    reporter = relationship("User", foreign_keys=[reporter_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    project = relationship("Project", back_populates="reports")
