from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AppealBase(BaseModel):
    type: str = Field(..., description="申诉类型: account/content/other")
    title: str = Field(..., min_length=1, max_length=200, description="申诉标题")
    description: str = Field(..., min_length=1, description="申诉描述")
    attachments: Optional[List[str]] = Field(default=[], description="附件URL列表")


class AppealCreate(AppealBase):
    pass


class AppealUpdate(BaseModel):
    status: Optional[str] = Field(None, description="状态: pending/processing/resolved/rejected")
    admin_response: Optional[str] = Field(None, description="管理员回复")


class AppealResponse(AppealBase):
    id: int
    user_id: int
    status: str
    admin_response: Optional[str] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppealWithUser(AppealResponse):
    user: dict = Field(..., description="申诉用户信息")
