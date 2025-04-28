from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.params import Security
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import  get_db
from app.models import  Users
from app.schemas import UserOut, RegisterUser, UserUpdate, LoginUser
from app.utils.hashing import hash_password, verify_password
from app.utils.tokens import create_access_token
from app.auth import get_current_user

router = APIRouter(tags=["Users"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/user_registration", response_model=UserOut)
def register_user(data: RegisterUser, db: Session = Depends(get_db)):
    hash_pw = hash_password(data.password)
    usr = Users(username = data.username, hashed_password= hash_pw, user_mail = data.user_mail, is_admin=True)
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr


@router.put("/user_update/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), current_user: Users =  Depends(get_current_user)):
    usr = db.query(Users).get(user_id)
    if not usr:
        raise HTTPException(status_code=404, detail="User not found")
    if data.username is not None:
        usr.username = data.username
    if data.user_mail is not None:
        usr.user_mail = data.user_mail
    db.commit()
    db.refresh(usr)
    return usr

