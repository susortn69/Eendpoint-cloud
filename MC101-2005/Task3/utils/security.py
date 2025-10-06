from datetime import datetime, timezone, timedelta
from typing import Generator

from fastapi import Depends, Header, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlalchemy.orm import Session

from api.users.UserDBModels import User
from config import Settings
from utils.constants import ResponseMessages
from utils.database import get_db

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def hash_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt", "pbkdf2_sha256", "argon2"], deprecated="auto")


def hash_password(password: SecretStr | str) -> str:
    value = password.get_secret_value() if isinstance(password, SecretStr) else str(password)
    return hash_context().hash(value)


def verify_password(plain_password: SecretStr | str, hashed_password: str) -> bool:
    value = plain_password.get_secret_value() if isinstance(plain_password, SecretStr) else str(plain_password)
    return hash_context().verify(value, hashed_password)


def create_access_token(data: dict) -> str:
    data_to_encode = data.copy()
    expire = timedelta(minutes=settings.JWT_EXPIRATION_TIME)
    expire_time = datetime.now(timezone.utc) + expire
    data_to_encode.update({"exp": expire_time.timestamp()})
    encoded_jwt = jwt.encode(
        data_to_encode,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM],
        )
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessages.INVALID_TOKEN_MISSING_EMAIL)
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessages.INVALID_TOKEN_MISSING_USER)
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessages.INVALID_TOKEN) from None


def ensure_active_user(current_user: User = Depends(decode_access_token)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ResponseMessages.USER_INACTIVE)
    return current_user


def require_admin(x_admin_token: str = Header(..., alias="X-Admin-Token")) -> None:
    if x_admin_token != settings.ADMIN_API_TOKEN.get_secret_value():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ResponseMessages.ADMIN_UNAUTHORIZED)
