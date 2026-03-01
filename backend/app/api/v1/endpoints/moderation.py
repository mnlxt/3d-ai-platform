from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.session import get_db
from app.models.content_report import ContentReport
from app.models.project import Project
from app.models.user import User
from app.schemas.content_report import ContentReportCreate, ContentReportUpdate, ContentReportResponse, ContentReportWithDetails
from app.schemas.project import ProjectResponse
from app.core.security import get_current_user, require_admin
from datetime import datetime

router = APIRouter()


@router.post("/reports", response_model=ContentReportResponse)
async def create_report(
    report_data: ContentReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == report_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在"
        )
    
    existing_report = db.query(ContentReport).filter(
        ContentReport.reporter_id == current_user.id,
        ContentReport.project_id == report_data.project_id,
        ContentReport.status == "pending"
    ).first()
    
    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已举报过该作品，请等待处理结果"
        )
    
    report = ContentReport(
        reporter_id=current_user.id,
        project_id=report_data.project_id,
        reason=report_data.reason,
        description=report_data.description
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return report


@router.get("/reports", response_model=List[ContentReportWithDetails])
async def list_reports(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(ContentReport).join(User, ContentReport.reporter_id == User.id)
    
    if status:
        query = query.filter(ContentReport.status == status)
    
    reports = query.order_by(ContentReport.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for report in reports:
        report_dict = ContentReportResponse.from_orm(report).dict()
        report_dict["reporter"] = {
            "id": report.reporter.id,
            "username": report.reporter.username,
            "email": report.reporter.email
        }
        report_dict["project"] = {
            "id": report.project.id,
            "title": report.project.title,
            "owner_id": report.project.owner_id
        }
        result.append(report_dict)
    
    return result


@router.get("/reports/{report_id}", response_model=ContentReportWithDetails)
async def get_report(
    report_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    report = db.query(ContentReport).filter(ContentReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="举报不存在"
        )
    
    report_dict = ContentReportResponse.from_orm(report).dict()
    report_dict["reporter"] = {
        "id": report.reporter.id,
        "username": report.reporter.username,
        "email": report.reporter.email
    }
    report_dict["project"] = {
        "id": report.project.id,
        "title": report.project.title,
        "owner_id": report.project.owner_id
    }
    
    return report_dict


@router.put("/reports/{report_id}", response_model=ContentReportResponse)
async def update_report(
    report_id: int,
    report_data: ContentReportUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    report = db.query(ContentReport).filter(ContentReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="举报不存在"
        )
    
    if report_data.status:
        if report_data.status not in ["pending", "reviewed", "dismissed"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的状态值"
            )
        report.status = report_data.status
        report.reviewed_by = current_user.id
        report.reviewed_at = datetime.utcnow()
    
    if report_data.admin_notes is not None:
        report.admin_notes = report_data.admin_notes
    
    if report_data.action_taken:
        if report_data.action_taken not in ["none", "warning", "removed", "banned"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的处理措施"
            )
        report.action_taken = report_data.action_taken
        
        if report_data.action_taken == "removed":
            project = db.query(Project).filter(Project.id == report.project_id).first()
            if project:
                project.is_public = False
    
    db.commit()
    db.refresh(report)
    
    return report


@router.get("/admin/projects", response_model=List[ProjectResponse])
async def list_all_projects(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    return projects


@router.put("/admin/projects/{project_id}/status")
async def update_project_status(
    project_id: int,
    is_public: bool,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在"
        )
    
    project.is_public = is_public
    db.commit()
    db.refresh(project)
    
    status_text = "上架" if is_public else "下架"
    return {"message": f"作品{status_text}成功", "project": ProjectResponse.from_orm(project)}


@router.get("/admin/stats")
async def get_moderation_stats(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    pending_reports = db.query(ContentReport).filter(ContentReport.status == "pending").count()
    total_reports = db.query(ContentReport).count()
    reviewed_reports = db.query(ContentReport).filter(ContentReport.status == "reviewed").count()
    dismissed_reports = db.query(ContentReport).filter(ContentReport.status == "dismissed").count()
    
    return {
        "pending_reports": pending_reports,
        "total_reports": total_reports,
        "reviewed_reports": reviewed_reports,
        "dismissed_reports": dismissed_reports
    }
