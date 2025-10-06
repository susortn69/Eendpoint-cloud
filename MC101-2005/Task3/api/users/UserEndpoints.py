from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.users.UserDBModels import User
from utils.constants import Endpoints, ResponseMessages
from utils.database import get_db
from utils.security import (
    create_access_token,
    ensure_active_user,
    hash_password,
    verify_password,
)
from .UserSchemas import (
    UserLoginSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateSchema,
)


UserRouter = APIRouter(prefix="/users", tags=["Users"])


@UserRouter.post(Endpoints.REGISTER, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            detail=ResponseMessages.USER_ALREADY_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_active=user.is_active,
    )
    db.add(new_user)
    db.commit()
    return {"message": ResponseMessages.USER_CREATED}


@UserRouter.post(Endpoints.LOGIN)
def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(
            detail=ResponseMessages.USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            detail=ResponseMessages.INVALID_PASSWORD,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    payload = {"user_id": existing_user.id, "email": existing_user.email}
    token = create_access_token(data=payload)
    return {"message": ResponseMessages.LOGIN_SUCCESS, "access_token": token, "token_type": "bearer"}


@UserRouter.patch(Endpoints.USER_UPDATE)
def update_user(
    update: UserUpdateSchema,
    current_user: User = Depends(ensure_active_user),
    db: Session = Depends(get_db),
):
    current_user = db.merge(current_user)

    if update.email and update.email != current_user.email:
        email_exists = db.query(User).filter(User.email == update.email).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ResponseMessages.USER_ALREADY_EXISTS,
            )
        current_user.email = update.email

    if update.name:
        current_user.name = update.name

    if update.password:
        current_user.hashed_password = hash_password(update.password)

    if update.is_active is not None:
        current_user.is_active = update.is_active

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {
        "message": ResponseMessages.USER_UPDATED,
        "user": UserPublicSchema.model_validate(current_user),
    }


@UserRouter.delete(Endpoints.USER_DELETE, status_code=status.HTTP_200_OK)
def delete_user_account(current_user: User = Depends(ensure_active_user), db: Session = Depends(get_db)):
    current_user = db.merge(current_user)
    db.delete(current_user)
    db.commit()
    return {"message": ResponseMessages.USER_DELETED}


@UserRouter.get(Endpoints.USER_INFO)
def get_user_info(current_user: User = Depends(ensure_active_user)):
    return UserPublicSchema.model_validate(current_user).model_dump()
