import app.api.managers.user as user_manager
import app.api.managers.parameter as parameter_manager
# import numpy as np

from app.api.model.UserModel import UserDB, UserSchema, UserLoginSchema
from app.api.model.CalculatorModel import CalculatorSchema,WholeDaysAheadSchema
from pydantic import BaseModel, Field, NonNegativeInt, EmailStr

from fastapi import APIRouter, HTTPException, Path, status, Depends
from fastapi.responses import JSONResponse
from app.utils.exceptions import user_exceptions
from typing import List, Annotated
from sqlalchemy import (Column, Integer, Boolean, String, Table, create_engine, MetaData)
from app.api.model.UserModel import UserUpdateSchema
from datetime import datetime as dt
from app.api.utils.jwt_auth_handler import signJWT, decodeJWT
from app.core.common import ErrorCode
from app.api.utils.calculator.basic_functions import *
from app.api.utils.calculator.vintages import *
from app.api.utils.jwt_auth_handler import JWTBearer
from app.api.utils.calcFunctions.ControlAccounts import getCashWaterfallItemsData
import app.api.utils.calcFunctions.basicAssumptions as basInputs


from app.api.utils.calcFunctions.test import test

import os

import json
router = APIRouter()
def records_to_json(records):
    # Convert each record to a dictionary and return a JSON string
    return json.dumps([dict(record) for record in records], indent=4)

def get_cur_path():
    return os.path.dirname(os.path.realpath(__file__))

@router.post("/test") 
async def testFunc(parameter_id: int):
    data =  await parameter_manager.get_parameter_info_list_by_parameter_id(parameter_id)
    file_name = 'project_parameters.json'
    current_dir = get_cur_path()
    f = open(current_dir + '/' + file_name, 'w')
    f.write(records_to_json(data))
    f.close()
    # # Write the JSON data to a file
    # f = open(current_dir + '/' + file_name, 'r')
    # val = json.load(f)
    print("debug from update json and calling basInputs initial function - 1")
    basInputs.initial()
    print("debug from update json and calling basInputs initial function - 2")
    return test()
    # return getCashWaterfallItemsData()
   

