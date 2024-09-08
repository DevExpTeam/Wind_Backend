import app.api.managers.user as user_manager
from app.api.model.UserModel import UserDB, UserSchema, UserLoginSchema
from fastapi import APIRouter, HTTPException, Path, status, Depends
from fastapi.responses import JSONResponse
from app.utils.exceptions import user_exceptions
from typing import List, Annotated
from sqlalchemy import (Column, Integer, Boolean, String, Table, create_engine, MetaData)
from app.api.model.UserModel import UserUpdateSchema
from datetime import datetime as dt
from app.api.utils.jwt_auth_handler import signJWT, decodeJWT
from app.core.common import ErrorCode
from app.api.utils.jwt_auth_handler import JWTBearer
router = APIRouter()

@router.get("/get-all")
async def get_all_user():
    res = await user_manager.get_all_user()
    return res
 

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_user(id: int, payload: UserUpdateSchema, current_user: Annotated[str, Depends(user_manager.get_current_user)]):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": ErrorCode.FORBIDDEN
            },
        )   
    updated = await user_manager.update_user(user_id=id, payload=payload)
    if updated:
        return {"msg": "Success Update."}
    return  {"msg": "Error."}


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user(id: int, current_user: Annotated[str, Depends(user_manager.get_current_user)]):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": ErrorCode.FORBIDDEN
            },
        )   
    deleted = await user_manager.delete_user(user_id=id)
    if deleted:
        return {"msg": "Success Delete."}
    return  {"msg": "Error."}



# #DELETE route
# @router.delete("/deleteFromId/{id}", response_model=UserDB)
# async def delete_user_from_id(id: int):
#     param = await crudUser.getUserFromId(id)
#     if not param:
#         raise HTTPException(status_code=404, detail="item not found")
#     await crudUser.deleteUserFromId(id)

#     return param

