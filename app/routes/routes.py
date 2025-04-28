# from fastapi import APIRouter, Request, Depends, HTTPException, status
# from fastapi.params import Security
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from app.database import SessionLocal, get_db
# from app.models import Project, Users
# from app.schemas import ProjectCreate, ProjectOut, ProjectUpdate, UserOut, RegisterUser, UserUpdate, LoginUser
# from app.utils.hashing import hash_password, verify_password
# from app.utils.tokens import create_access_token
# from app.auth import get_current_user
#
#
#
#
# router = APIRouter()
# templates = Jinja2Templates(directory="app/templates")
#
#
#
# @router.get("/", tags=["Main"])
# def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
#
# @router.post("/projects", response_model=ProjectOut, tags=["Projects"])
# def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
#     proj = Project(**data.dict())
#     db.add(proj)
#     db.commit()
#     db.refresh(proj)
#     return proj
#
# @router.get("/projects", response_model=list[ProjectOut], tags=["Projects"])
# def read_projects(db: Session = Depends(get_db)):
#     return db.query(Project).all()
#
# @router.get("/projects/{project_id}", response_model=ProjectOut, tags=["Projects"])
# def read_project(project_id: int, db: Session = Depends(get_db)):
#     proj = db.query(Project).get(project_id)
#     if not proj:
#         raise HTTPException(404, "Project not found")
#     return proj
#
# @router.put("/projects/{project_id}", response_model=ProjectOut, tags=["Projects"])
# def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
#     proj = db.query(Project).get(project_id)
#     if not proj:
#         raise HTTPException(404, "Project not found")
#     for field, value in data.dict(exclude_unset=True).items():
#         setattr(proj, field, value)
#     db.commit()
#     db.refresh(proj)
#     return proj
#
# @router.delete("/projects/{project_id}", status_code=204, tags=["Projects"])
# def delete_project(project_id: int, db: Session = Depends(get_db)):
#     proj = db.query(Project).get(project_id)
#     if not proj:
#         raise HTTPException(404, "Project not found")
#     db.delete(proj)
#     db.commit()
#
#
# @router.post("/user_registration", response_model=UserOut, tags=["User"])
# def register_user(data: RegisterUser, db: Session = Depends(get_db)):
#     hash_pw = hash_password(data.password)
#     usr = Users(username = data.username, hashed_password= hash_pw, user_mail = data.user_mail, is_admin=True)
#     db.add(usr)
#     db.commit()
#     db.refresh(usr)
#     return usr
#
#
# @router.put("/user_update/{user_id}", response_model=UserOut, tags=["User"])
# def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), current_user: Users =  Depends(get_current_user)):
#     usr = db.query(Users).get(user_id)
#     if not usr:
#         raise HTTPException(status_code=404, detail="User not found")
#     if data.username is not None:
#         usr.username = data.username
#     if data.user_mail is not None:
#         usr.user_mail = data.user_mail
#     db.commit()
#     db.refresh(usr)
#     return usr
#
# @router.post("/login", tags=["Auth"])
# def login(data: LoginUser, db: Session = Depends(get_db)):
#     user = db.query(Users).filter(Users.user_mail == data.user_mail).first()
#     if not user or not verify_password(data.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": str(user.id)})
#     return {"access_token": access_token, "token_type": "bearer"}