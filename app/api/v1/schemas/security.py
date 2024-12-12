from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class Permission(str, Enum):
    ADMINISTRATOR = 'administrator'
    OPERATOR = 'operator'
    DRIVER = 'driver'
    API = 'api'


class TokenSchema(BaseModel):
    access_token: str
    permission: str
    token_type: str


class UserSchema(BaseModel):
    username: str
    last_name: Optional[str]
    first_name: Optional[str]
    email: Optional[EmailStr]
    permission: Permission
    city: Optional[str]
    last_visit: Optional[datetime]


class UserDBSchema(UserSchema):
    password_hash: str

    class Config:
        from_attributes = True
