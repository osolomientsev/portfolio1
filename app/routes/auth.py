from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from app.database import  get_db
from app.models import  Users
from app.schemas import  LoginUser
from app.utils.hashing import verify_password
from app.utils.tokens import create_access_token

router = APIRouter(prefix="/login", tags=["Auth"])

@router.post("")
def login(data: LoginUser, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user_mail == data.user_mail).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"user_id":user.id,"access_token": access_token, "token_type": "bearer"}