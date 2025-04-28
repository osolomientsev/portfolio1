from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.params import Security
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectOut, ProjectUpdate


router = APIRouter(prefix="/projects", tags=["Projects"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", tags=["Main"])
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("", response_model=ProjectOut)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    proj = Project(**data.dict())
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@router.get("", response_model=list[ProjectOut])
def read_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.get("", response_model=ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(404, "Project not found")
    return proj

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(404, "Project not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(proj, field, value)
    db.commit()
    db.refresh(proj)
    return proj

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(404, "Project not found")
    db.delete(proj)
    db.commit()