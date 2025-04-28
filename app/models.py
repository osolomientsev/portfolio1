from sqlalchemy import Column, Integer, String, Text, Boolean
from .database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String, index=True)
    description = Column(Text)
    link = Column(String)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password  = Column(String)
    user_mail = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
