from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    is_active: bool = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
    is_active: Optional[bool] = None


class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
