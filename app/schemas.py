from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    title: str
    description: str
    link: str


class ProjectOut(ProjectCreate):
    id: int

    class Config:
        orm_mode = True

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    link: str | None = None


class RegisterUser(BaseModel):
    username: str
    password: str
    user_mail: str


class UserOut(BaseModel):
    id: int
    username : str
    user_mail : str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    user_mail: str | None = Field(default=None, min_length=5, max_length=100)


class LoginUser(BaseModel):
    user_mail: str
    password: str