from pydantic import BaseModel, Field, NonNegativeInt, EmailStr
from datetime import datetime as dt
from pytz import timezone as tz
from typing import Optional

class UserSchema(BaseModel): 
    email: str
    password : str  
    is_admin: Optional[bool] = False
    param: Optional[dict] = {}
    enabled: Optional[bool] = False
    created_at: Optional[str] = dt.now().strftime("%Y-%m-%d %H:%M")
    updated_at: Optional[str] = dt.now().strftime("%Y-%m-%d %H:%M")
 
    class Config:  
        json_schema_extra={
            "example": {
                "email": "test@gmail.com",
                "password":"password"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config: 
        json_schema_extra={
            "example": {
                "email": "test@gmail.com",
                "password":"password"
            }
        }


class UserUpdateSchema(BaseModel): 
    password: Optional[str] = None
    enabled: Optional[bool] = None
    param: Optional[dict] = None

    class Config: 
        json_schema_extra={
            "example": { 
                "password":"password",
                "enabled": True
            }
        }

class UserParamUpdateSchema(BaseModel):   
    parameter_id: int

    class Config: 
        json_schema_extra={
            "example": { 
                "parameter_id": 1
            }
        }


class UserDB(UserSchema):
    id: int 
