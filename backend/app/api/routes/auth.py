import app.api.managers.user as user_manager
from app.api.model.UserModel import UserDB, UserSchema, UserLoginSchema
from fastapi import APIRouter, HTTPException, Path, status, Depends
from app.utils.exceptions import user_exceptions
from typing import List 
from datetime import datetime as dt
from app.api.utils.jwt_auth_handler import signJWT
from app.core.common import ErrorCode 
from app.api.utils.jwt_auth_handler import JWTBearer
router = APIRouter()

@router.post("/signup", status_code=201)
async def create_new_user(payload: UserSchema):
    try:
        created_user = await user_manager.create(payload)
    except user_exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail={
                "code": ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                "message": "Alreay registered!"
             },
        )
    except user_exceptions.InvalidPassword as e:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )  
    return signJWT(created_user)


@router.post("/signin")
async def login(userInfo: UserLoginSchema):
    try:
        user = await user_manager.login(userInfo)
    except user_exceptions.UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": ErrorCode.USER_NOT_FOUND
            },
        )  
    except user_exceptions.UserNotAllowed:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail={
                "code": ErrorCode.USER_NOT_ALLOWED,
                "message": "User not allowed!"
            },
        )  
    except user_exceptions.InvalidPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "message": "Invalid Password!"
            },
        )   
    return signJWT(user)

