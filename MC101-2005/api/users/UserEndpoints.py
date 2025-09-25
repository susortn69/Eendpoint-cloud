from fastapi import APIRouter, Depends, HTTPException, status

from api.users.UserDBModels import add_user, delete_user, get_user_by_email, UserDBModel
from utils.constants import Endpoints, ResponseMessages
from utils.security import create_access_token, decode_access_token, hash_password, verify_password
from .UserSchemas import UserLoginSchema, UserSchema


UserRouter = APIRouter(prefix="/users", tags=["Users"])


@UserRouter.post(Endpoints.REGISTER, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    """Register a new user if the email is not already taken."""
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            detail=ResponseMessages.USER_ALREADY_EXISTS,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    add_user(
        UserDBModel(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password),
            is_active=user.is_active,
        )
    )
    return {"message": ResponseMessages.USER_CREATED}


@UserRouter.post(Endpoints.LOGIN)
def login_user(user: UserLoginSchema):
    """Authenticate the user and return an access token."""
    existing_user = get_user_by_email(user.email)
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

    payload = {"user_id": str(existing_user.id), "email": existing_user.email}
    token = create_access_token(data=payload)
    return {"message": ResponseMessages.LOGIN_SUCCESS, "access_token": token, "token_type": "bearer"}


@UserRouter.delete(Endpoints.USER_DELETE, status_code=status.HTTP_200_OK)
def delete_user_account(payload: dict = Depends(decode_access_token)):
    """Delete the currently authenticated user."""
    user_id = payload.get("user_id")
    email = payload.get("email")
    if user_id is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ResponseMessages.INVALID_TOKEN,
        )

    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            detail=ResponseMessages.USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ResponseMessages.INVALID_TOKEN,
        )

    if user.id != user_id_int:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ResponseMessages.INVALID_TOKEN,
        )

    if not delete_user(user_id_int):
        raise HTTPException(
            detail=ResponseMessages.USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return {"message": ResponseMessages.USER_DELETED}


@UserRouter.get(Endpoints.USER_INFO)
def get_user_info(payload: dict = Depends(decode_access_token)):
    """Return the payload extracted from the caller's access token."""
    return payload
