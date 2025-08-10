from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    chat_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: str

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    chat_id: int
    first_name: str
    phone_number: str


class UserReadSchema(BaseModel):
    id: int
    chat_id: int
