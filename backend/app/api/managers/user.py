from app.api.model.UserModel import *
from app.db import  database, user
from datetime import datetime as dt
from sqlalchemy import and_ 
from app.utils.exceptions import user_exceptions
import bcrypt
from typing import Annotated
from fastapi import Depends
from app.api.utils.jwt_auth_handler import JWTBearer, decodeJWT


def get_hashed_password(plain_text_password: str):
      # Hash a password for the first time
      #   (Using bcrypt, the salt is saved into the hash itself)
      return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password( plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

# def check_password( plain_text_password, hashed_password):
#     # Check hashed password. Using bcrypt, the salt is saved into the hash itself
#     return plain_text_password.encode('utf-8') == hashed_password.encode('utf-8')

async def create(payload: UserSchema):
    created_at = dt.now().strftime("%Y-%m-%d %H:%M")
    updated_at = dt.now().strftime("%Y-%m-%d %H:%M")  
    existingUser = await database.fetch_one(query=user.select().where(payload.email == user.c.email))
    if existingUser:
        raise user_exceptions.UserAlreadyExists
    insert_payload = {
        "email": payload.email,
        "password": get_hashed_password(payload.password),
        "is_admin": False,
        "enabled": True,
        "parameter_id": 0,
        "created_at": created_at,
        "updated_at": updated_at
    }
    try: 
        created_user_id = await database.execute(user.insert().values(insert_payload))  
    except Exception as e:
        raise 
    return {
        "id" : created_user_id,
        "email": payload.email,
        "is_admin": False
    }

async def login(userInfo: UserSchema):
    user = await get_user_by_email(userInfo.email)
    if user is None:
        raise user_exceptions.UserNotFound 
    if not user.enabled:
        raise user_exceptions.UserNotAllowed
    if not check_password(userInfo.password, user.password):
        raise user_exceptions.InvalidPassword
    return user

async def update_user(user_id: int, payload: UserUpdateSchema):
    update_payload = {}
    if payload.password is not None:
        update_payload["password"] = get_hashed_password(payload.password)
    if payload.enabled is not None:
        update_payload["enabled"] = payload.enabled 
    update_query = user.update().where(user_id == user.c.id).values(update_payload)
    try: 
        res = await database.execute(update_query)
    except Exception as e:
        return False
    return True


async def update_user_param(user_id: int, payload: UserParamUpdateSchema): 
    update_payload = {
        'parameter_id': payload.parameter_id
    }
    update_query = user.update().where(user_id == user.c.id).values(update_payload)
    try: 
        res = await database.execute(update_query)
    except Exception as e:
        return False
    return True

async def delete_user(user_id: int):
    delete_query = user.delete().where(user_id == user.c.id) 
    try: 
        res = await database.execute(delete_query)
    except Exception as e:
        return False
    return True
 
async def get_user_by_email(email: str):
    query = user.select().where(email == user.c.email)
    return await database.fetch_one(query=query)

async def get_all_user(): 
    query = user.select()
    users = await database.fetch_all(query=query)
    filterd_users = []
    for u in users:
        filterd_users.append({
            "id": u.id,
            "email": u.email,
            "enabled": u.enabled,
            "created_at": u.created_at,
            "updated_at": u.updated_at
        })
    return filterd_users

async def getUserFromId(id: int):
    query = user.select().where(id == user.c.id)
    return await database.fetch_one(query=query)

async def deleteUserFromId(id:int):
    query = user.delete().where(id == user.c.id)
    return await database.execute(query=query)


async def get_current_user(token: Annotated[str, Depends(JWTBearer())]):
    user = decodeJWT(token)
    return user