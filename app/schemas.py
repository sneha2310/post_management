from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  # This allows the model to read data even if it is not a dict, but an ORM model instance


class PostResponse(Post):
    id: int
    owner_id: int
    owner: UserResponse

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # 1 for like, 0 for unlike

    class Config:
        orm_mode = True  # This allows the model to read data even if it is not a dict, but an ORM model instance