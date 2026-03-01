from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.user import User
from app.models.project import Project
from app.models.appeal import Appeal
from app.models.content_report import ContentReport
from app.core.security import require_admin

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    
    total_users = db.query(User).count()
    new_users_today = db.query(User).filter(User.created_at >= today_start).count()
    
    total_projects = db.query(Project).count()
    new_projects_today = db.query(Project).filter(Project.created_at >= today_start).count()
    
    pending_appeals = db.query(Appeal).filter(Appeal.status == "pending").count()
    pending_reports = db.query(ContentReport).filter(ContentReport.status == "pending").count()
    
    user_roles = db.query(User.role, func.count(User.id)).group_by(User.role).all()
    role_distribution = {role: count for role, count in user_roles}
    
    project_status = db.query(Project.status, func.count(Project.id)).group_by(Project.status).all()
    status_distribution = {status: count for status, count in project_status}
    
    return {
        "users": {
            "total": total_users,
            "new_today": new_users_today,
            "role_distribution": role_distribution
        },
        "projects": {
            "total": total_projects,
            "new_today": new_projects_today,
            "status_distribution": status_distribution
        },
        "pending_tasks": {
            "appeals": pending_appeals,
            "reports": pending_reports
        }
    }


@router.get("/stats/users")
async def get_user_stats(
    days: int = 7,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days-1)
    
    daily_stats = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_start = datetime.combine(date, datetime.min.time())
        date_end = datetime.combine(date + timedelta(days=1), datetime.min.time())
        
        count = db.query(User).filter(
            and_(User.created_at >= date_start, User.created_at < date_end)
        ).count()
        
        daily_stats.append({
            "date": date.isoformat(),
            "count": count
        })
    
    return {
        "period": f"{start_date.isoformat()} to {end_date.isoformat()}",
        "daily_stats": daily_stats
    }


@router.get("/stats/projects")
async def get_project_stats(
    days: int = 7,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days-1)
    
    daily_stats = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_start = datetime.combine(date, datetime.min.time())
        date_end = datetime.combine(date + timedelta(days=1), datetime.min.time())
        
        count = db.query(Project).filter(
            and_(Project.created_at >= date_start, Project.created_at < date_end)
        ).count()
        
        daily_stats.append({
            "date": date.isoformat(),
            "count": count
        })
    
    return {
        "period": f"{start_date.isoformat()} to {end_date.isoformat()}",
        "daily_stats": daily_stats
    }


@router.get("/stats/activity")
async def get_activity_stats(
    days: int = 7,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days-1)
    
    daily_activity = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_start = datetime.combine(date, datetime.min.time())
        date_end = datetime.combine(date + timedelta(days=1), datetime.min.time())
        
        new_users = db.query(User).filter(
            and_(User.created_at >= date_start, User.created_at < date_end)
        ).count()
        
        new_projects = db.query(Project).filter(
            and_(Project.created_at >= date_start, Project.created_at < date_end)
        ).count()
        
        daily_activity.append({
            "date": date.isoformat(),
            "new_users": new_users,
            "new_projects": new_projects
        })
    
    return {
        "period": f"{start_date.isoformat()} to {end_date.isoformat()}",
        "daily_activity": daily_activity
    }


@router.get("/recent/appeals")
async def get_recent_appeals(
    limit: int = 5,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    appeals = db.query(Appeal).order_by(Appeal.created_at.desc()).limit(limit).all()
    
    result = []
    for appeal in appeals:
        result.append({
            "id": appeal.id,
            "title": appeal.title,
            "type": appeal.type,
            "status": appeal.status,
            "user": {
                "id": appeal.user.id,
                "username": appeal.user.username
            },
            "created_at": appeal.created_at.isoformat()
        })
    
    return result


@router.get("/recent/reports")
async def get_recent_reports(
    limit: int = 5,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    reports = db.query(ContentReport).order_by(ContentReport.created_at.desc()).limit(limit).all()
    
    result = []
    for report in reports:
        result.append({
            "id": report.id,
            "reason": report.reason,
            "status": report.status,
            "reporter": {
                "id": report.reporter.id,
                "username": report.reporter.username
            },
            "project": {
                "id": report.project.id,
                "title": report.project.title
            },
            "created_at": report.created_at.isoformat()
        })
    
    return result
