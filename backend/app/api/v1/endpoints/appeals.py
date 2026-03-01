from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.appeal import Appeal
from app.models.user import User
from app.schemas.appeal import AppealCreate, AppealUpdate, AppealResponse, AppealWithUser
from app.core.security import get_current_user, require_admin
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=AppealResponse)
async def create_appeal(
    appeal_data: AppealCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if appeal_data.type not in ["account", "content", "other"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的申诉类型"
        )
    
    appeal = Appeal(
        user_id=current_user.id,
        type=appeal_data.type,
        title=appeal_data.title,
        description=appeal_data.description,
        attachments=appeal_data.attachments or []
    )
    
    db.add(appeal)
    db.commit()
    db.refresh(appeal)
    
    return appeal


@router.get("/my", response_model=List[AppealResponse])
async def get_my_appeals(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Appeal).filter(Appeal.user_id == current_user.id)
    
    if status:
        query = query.filter(Appeal.status == status)
    
    appeals = query.order_by(Appeal.created_at.desc()).all()
    return appeals


@router.get("/", response_model=List[AppealWithUser])
async def list_appeals(
    status: Optional[str] = None,
    type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(Appeal).join(User, Appeal.user_id == User.id)
    
    if status:
        query = query.filter(Appeal.status == status)
    
    if type:
        query = query.filter(Appeal.type == type)
    
    appeals = query.order_by(Appeal.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for appeal in appeals:
        appeal_dict = AppealResponse.from_orm(appeal).dict()
        appeal_dict["user"] = {
            "id": appeal.user.id,
            "username": appeal.user.username,
            "email": appeal.user.email,
            "avatar_url": appeal.user.avatar_url
        }
        result.append(appeal_dict)
    
    return result


@router.get("/{appeal_id}", response_model=AppealWithUser)
async def get_appeal(
    appeal_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申诉不存在"
        )
    
    appeal_dict = AppealResponse.from_orm(appeal).dict()
    appeal_dict["user"] = {
        "id": appeal.user.id,
        "username": appeal.user.username,
        "email": appeal.user.email,
        "avatar_url": appeal.user.avatar_url
    }
    
    return appeal_dict


@router.put("/{appeal_id}", response_model=AppealResponse)
async def update_appeal(
    appeal_id: int,
    appeal_data: AppealUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申诉不存在"
        )
    
    if appeal_data.status:
        if appeal_data.status not in ["pending", "processing", "resolved", "rejected"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的状态值"
            )
        appeal.status = appeal_data.status
        
        if appeal_data.status in ["resolved", "rejected"]:
            appeal.resolved_by = current_user.id
            appeal.resolved_at = datetime.utcnow()
    
    if appeal_data.admin_response is not None:
        appeal.admin_response = appeal_data.admin_response
    
    db.commit()
    db.refresh(appeal)
    
    return appeal


@router.delete("/{appeal_id}")
async def delete_appeal(
    appeal_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申诉不存在"
        )
    
    db.delete(appeal)
    db.commit()
    
    return {"message": "申诉删除成功"}
