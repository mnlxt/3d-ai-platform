from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ContentReportBase(BaseModel):
    project_id: int = Field(..., description="被举报的作品ID")
    reason: str = Field(..., min_length=1, max_length=500, description="举报原因")
    description: Optional[str] = Field(None, description="详细描述")


class ContentReportCreate(ContentReportBase):
    pass


class ContentReportUpdate(BaseModel):
    status: Optional[str] = Field(None, description="状态: pending/reviewed/dismissed")
    admin_notes: Optional[str] = Field(None, description="管理员备注")
    action_taken: Optional[str] = Field(None, description="处理措施: none/warning/removed/banned")


class ContentReportResponse(ContentReportBase):
    id: int
    reporter_id: int
    status: str
    admin_notes: Optional[str] = None
    action_taken: str
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentReportWithDetails(ContentReportResponse):
    reporter: dict = Field(..., description="举报人信息")
    project: dict = Field(..., description="被举报作品信息")
