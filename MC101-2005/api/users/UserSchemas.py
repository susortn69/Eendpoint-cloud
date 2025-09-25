from pydantic import BaseModel, EmailStr, SecretStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    is_active: bool = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr