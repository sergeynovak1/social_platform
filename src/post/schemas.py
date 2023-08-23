from pydantic import BaseModel
from datetime import datetime

from src.auth.schemas import UserOut


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostExample(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class PostOut(Post):
    votes: int

    class Config:
        from_attributes = True
