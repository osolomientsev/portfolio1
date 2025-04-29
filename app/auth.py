from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Users
from app.utils.tokens import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    user = db.query(Users).get(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
