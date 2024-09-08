from pydantic import BaseModel, Field, NonNegativeInt
from datetime import datetime as dt
from pytz import timezone as tz
from typing import Optional
import enum

class ParameterSchema(BaseModel):
    clone_id: Optional[int] = -1
    user_id: Optional[int]  = 0
    title: str = ''
    description: str = ''
    created_at: Optional[str] = dt.now().strftime("%Y-%m-%d %H:%M")
    updated_at: Optional[str] = dt.now().strftime("%Y-%m-%d %H:%M")
 


class ParameterDB(ParameterSchema):
    id: int 


class ParameterInfoSchema(BaseModel):
    parameter_id : int
    param_index: str
    value : dict

    created_at: Optional[str] = dt.now().strftime("%Y-%m-%d %H:%M")
    updated_at: Optional[str] = dt.now().strftime("%Y-%m-%d %H:%M")
 

class ParameterInfoDB(ParameterInfoSchema):
    id: int 


# # This is the schema for history list
# class OperationHistoryListSchema(BaseModel):
#     date: str
#     name : str


# class OperationHistoryListDB(OperationHistoryListSchema):
#     id : int


# # This is the schema for all history data
# class OperationHistoryDataSchema(BaseModel):
#     date : str
#     name : str
#     title: str  # this is the param's name (for.e.g BaseCurrencyLabel)
#     category: str   #this will be the category in which part this is included
#     value : str
#     type: str


# class OperationHistoryDataDB(OperationHistoryDataSchema):
#     id : int
