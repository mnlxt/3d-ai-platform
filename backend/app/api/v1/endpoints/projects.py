from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectStatusUpdate,
    ProjectResponse,
    ProjectListResponse,
)
from app.core.security import get_current_user, require_admin

router = APIRouter()


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    status: Optional[str] = Query(None, description="按状态筛选"),
    search: Optional[str] = Query(None, description="按名称搜索"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(12, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Project).filter(Project.user_id == current_user.id)
    
    # 状态筛选
    if status:
        query = query.filter(Project.status == status)
    
    # 名称搜索
    if search:
        query = query.filter(Project.name.contains(search))
    
    # 排序
    if sort_order == "desc":
        query = query.order_by(getattr(Project, sort_by).desc())
    else:
        query = query.order_by(getattr(Project, sort_by).asc())
    
    # 分页
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return ProjectListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        user_id=current_user.id,
        status="draft",
        model_data={
            "model": None,
            "textures": [],
            "skeleton": None,
            "animations": [],
            "render_settings": {}
        },
        storage_paths={
            "minio_bucket": "user-projects",
            "model_key": None,
            "texture_keys": [],
            "animation_keys": []
        }
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project


# ========== 管理员接口 ==========

@router.get("/all", response_model=list[ProjectResponse])
async def get_all_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    is_public: Optional[bool] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """管理员获取所有作品列表"""
    query = db.query(Project)
    
    if status:
        query = query.filter(Project.status == status)
    
    if is_public is not None:
        query = query.filter(Project.is_public == is_public)
    
    projects = query.offset(skip).limit(limit).all()
    return projects


@router.put("/{project_id}/public", response_model=ProjectResponse)
async def toggle_project_public(
    project_id: int,
    is_public: bool,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """管理员设置作品公开/私密状态"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    project.is_public = is_public
    db.commit()
    db.refresh(project)
    
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    db.delete(project)
    db.commit()
    
    return {"message": "项目删除成功"}


@router.put("/{project_id}/status")
async def update_project_status(
    project_id: int,
    status_data: ProjectStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if status_data.status not in ["draft", "processing", "completed", "archived"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的项目状态"
        )
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    project.status = status_data.status
    db.commit()
    db.refresh(project)
    
    return {"message": "状态更新成功", "status": project.status}


@router.post("/{project_id}/duplicate", response_model=ProjectResponse)
async def duplicate_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    new_project = Project(
        name=f"{project.name} (副本)",
        description=project.description,
        user_id=current_user.id,
        status="draft",
        model_data=project.model_data.copy() if project.model_data else {},
        storage_paths={
            "minio_bucket": "user-projects",
            "model_key": None,
            "texture_keys": [],
            "animation_keys": []
        }
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project
