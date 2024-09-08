import app.api.managers.parameter as parameter_manager
import app.api.managers.user as user_manager

from app.api.model.parameterModel import ParameterDB, ParameterSchema, ParameterInfoDB, ParameterInfoSchema
from app.api.utils.constant import *
from fastapi import APIRouter, HTTPException, Path,status, Depends  
from typing import List, Annotated
from datetime import datetime as dt
from app.api.utils.jwt_auth_handler import JWTBearer
from app.api.model.UserModel import UserParamUpdateSchema
from app.core.common import ErrorCode


router = APIRouter()

@router.put("/update-user/{user_id}", dependencies=[Depends(JWTBearer())])
async def update_user(user_id: int, payload: UserParamUpdateSchema, current_user: Annotated[str, Depends(user_manager.get_current_user)]):
    updated = await user_manager.update_user_param(user_id=user_id, payload=payload)
    if updated:
        return payload

@router.get("/get-all", response_model=List[ParameterDB])
async def read_all_params():
    return await parameter_manager.get_all()

@router.post('/', dependencies=[Depends(JWTBearer())])
async def create_new_parameter(payload: ParameterSchema, current_user: Annotated[str, Depends(user_manager.get_current_user)]):
    return await parameter_manager.create_parameter(payload, user_id = current_user["user_id"])
 
@router.put('/{id}', dependencies=[Depends(JWTBearer())])
async def edit_parameter(id: int, payload: ParameterSchema, current_user: Annotated[str, Depends(user_manager.get_current_user)]):
    return await parameter_manager.edit_parameter(id, payload, user_id = current_user["user_id"])


@router.get('/get-by-user-id/{user_id}')
async def read_by_user_id(user_id: int):
    return await parameter_manager.get_parameter_list_by_user_id(user_id)

@router.post('/info' )
async def create_new_parameter_info(payload: ParameterInfoSchema):
    return await parameter_manager.create_or_update_parameter_info(payload)


@router.put('/info/{param_id}' )
async def update_parameter_info(param_id: int, payload: ParameterInfoSchema):
    return await parameter_manager.edit_parameter_info(param_id, payload)

@router.get('/info/get-all')
async def read_by_param_id(parameter_id: int): 
    return await parameter_manager.get_parameter_info_list_by_parameter_id(parameter_id)

@router.delete('/delete/{id}',dependencies=[Depends(JWTBearer())])
async def delete_by_id(id: int,current_user: Annotated[str, Depends(user_manager.get_current_user)]): 
    return await parameter_manager.delete_parameter(id,user_id = current_user["user_id"])
# @router.get("/{title}", response_model=ParamsDB)
# async def read_params_from_title(title: str):
#     param = await crudParams.getParamsFromTitle(title)
#     if not param:
#         raise HTTPException(status_code=404, detail="Param not found")
#     return param

# @router.get("/getParamsFromCategory/{category}", response_model=List[ParamsDB])
# async def read_params_from_category(category: str):
#     params = await crudParams.getParamsFromCategory(category)
#     return params

# @router.post("/", response_model=ParamsDB, status_code=201)
# async def create_new_param(payload: ParamsSchema):
#     paramId = await crudParams.post(payload)
#     created_date = dt.now().strftime("%Y-%m-%d %H:%M")

#     response_object = {
#         "id": paramId,
#         "user" : payload.user,
#         "title": payload.title,
#         "category": payload.category,
#         "value": payload.value,
#         "type" : payload.type,
#         "unit" : payload.unit,
#         "created_date": created_date,
#         "updated_date": created_date
#     }
#     return response_object


# #DELETE route
# @router.delete("/{title}", response_model=ParamsDB)
# async def delete_param_from_title(title: str):
#     param = await crudParams.getParamsFromTitle(title)
#     if not param:
#         raise HTTPException(status_code=404, detail="item not found")
#     await crudParams.deleteParamsFromTitle(title)

#     return param

# #DELETE route
# @router.delete("/deleteFromId/{id}", response_model=ParamsDB)
# async def delete_param_from_id(id: int):
#     param = await crudParams.getParamsFromId(id)
#     if not param:
#         raise HTTPException(status_code=404, detail="item not found")
#     await crudParams.deleteParamsFromId(id)

#     return param

# #Get the Basic Technoloty Input Params
# @router.get("/getCategoryParams/basicTechInput", response_model=List[ParamsDB])
# async def get_basic_input_params():
#     params = await crudParams.getParamsFromCategory(BASIC_TECH_INPUT_PARAMS)
#     return params


# #DELETE route
# @router.delete("/deleteCategoryParams/basicTechInput", response_model=List[ParamsDB])
# async def delete_basic_input_params():
#     params = await crudParams.getParamsFromCategory(BASIC_TECH_INPUT_PARAMS)
#     return params

# # Get the Battery Assumption Input Params
# @router.get("/getCategoryParams/batteryAssumInput", response_model=List[ParamsDB])
# async def get_battery_assumption_input_params():
#     params = await crudParams.getParamsFromCategory(BATTERY_ASSUM_INPUT_PARAMS)
#     return params

# # Delete the Battery Assumption Input Params
# @router.delete("/getCategoryParams/batteryAssumInput", response_model=List[ParamsDB])
# async def delete_battery_assumption_input_params():
#     params = await crudParams.getParamsFromCategory(BATTERY_ASSUM_INPUT_PARAMS)
#     return params


# # Get the Revenue Input Params
# @router.get("/getCategoryParams/revenueInput", response_model=List[ParamsDB])
# async def get_revenue_input_params():
#     params = await crudParams.getParamsFromCategory(REVUNE_INPUT_PARAMS)
#     return params

# # Delete the Revenue Input Params
# @router.delete("/getCategoryParams/revenueInput", response_model=List[ParamsDB])
# async def delete_revenue_input_params():
#     params = await crudParams.getParamsFromCategory(REVUNE_INPUT_PARAMS)
#     return params

# # Get the Cost of Sales Input Params
# @router.get("/getCategoryParams/costOfSalesInput", response_model=List[ParamsDB])
# async def get_cost_of_sales_input_params():
#     params = await crudParams.getParamsFromCategory("COST_OF_SALES_INPUT")
#     return params

# # Delete  the Cost of Sales Input Params
# @router.delete("/getCategoryParams/costOfSalesInput", response_model=List[ParamsDB])
# async def delete_cost_of_sales_input_params():
#     params = await crudParams.getParamsFromCategory("COST_OF_SALES_INPUT")
#     return params

# # Get the Administrative Costs Input Params
# @router.get("/getCategoryParams/adminnistrativeCostsInput", response_model=List[ParamsDB])
# async def get_administrative_costs_params():
#     params = await crudParams.getParamsFromCategory("ADMINISTRATIVE_COST_INPUT")
#     return params

# # Delete  the Administrative Costs Input Params
# @router.delete("/getCategoryParams/adminnistrativeCostsInput", response_model=List[ParamsDB])
# async def delete_administrative_costs_params():
#     params = await crudParams.getParamsFromCategory("ADMINISTRATIVE_COST_INPUT")
#     return params

# # Get the CAPEX Input Params
# @router.get("/getCategoryParams/capexAdditionCostsInput", response_model=List[ParamsDB])
# async def get_capex_addition_costs_params():
#     params = await crudParams.getParamsFromCategory("CAPEX_ADDITION_COST_INPUT")
#     return params

# # Delete the CAPEX Input Params
# @router.delete("/getCategoryParams/capexAdditionCostsInput", response_model=List[ParamsDB])
# async def delete_capex_addition_costs_params():
#     params = await crudParams.getParamsFromCategory("CAPEX_ADDITION_COST_INPUT")
#     return params

# # Get the CAPEX other Input Params
# @router.get("/getCategoryParams/capexOtherInput", response_model=List[ParamsDB])
# async def get_capex_other_input_params():
#     params = await crudParams.getParamsFromCategory("CAPEX_OTHER_INPUT")
#     return params

# # Delete the CAPEX other Input Params
# @router.delete("/getCategoryParams/capexOtherInput", response_model=List[ParamsDB])
# async def delete_capex_other_input_params():
#     params = await crudParams.getParamsFromCategory("CAPEX_OTHER_INPUT")
#     return params



