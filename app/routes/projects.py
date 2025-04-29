from fastapi import APIRouter, Request, Depends, HTTPException, status
#from fastapi.params import Security
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, Users
from app.schemas import ProjectCreate, ProjectOut, ProjectUpdate
from app.utils.permissions import check_role

#from fastapi.security import OAuth2PasswordBearer

from app.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])
templates = Jinja2Templates(directory="app/templates")

@router.post("", response_model=ProjectOut)
def create_project(data: ProjectCreate, db: Session = Depends(get_db),
                   current_user: Users =  Depends(get_current_user)):

    proj = Project(**data.model_dump(), user_id=current_user.id)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@router.get("", response_model=list[ProjectOut])
def read_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.get("/{project_id}", response_model=ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(404, "Project not found")
    return proj

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db),
                   current_user: Users =  Depends(get_current_user)):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(404, "Project not found")
    if proj.user_id != current_user.id and  not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    check_role(proj, current_user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(proj, field, value)
    db.commit()
    db.refresh(proj)
    return proj

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db),
                   current_user: Users =  Depends(get_current_user)):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(404, "Project not found")
    check_role(proj, current_user)
    db.delete(proj)
    db.commit()