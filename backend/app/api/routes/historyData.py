# import app.api.cruds.inputParams as crudParams
# from app.api.model.inputParamsModel import  OperationHistoryDataDB, OperationHistoryDataSchema
# from fastapi import APIRouter, HTTPException, Path
# from typing import List 
# from datetime import datetime as dt
# router = APIRouter()


# #This is for the history list when the user save the status



# # These are api routes for history lists
# @router.post("/", response_model=OperationHistoryDataDB, status_code=201)
# async def create_new_history_data(payload: OperationHistoryDataSchema):
#     paramId = await crudParams.postOperationHistoryData(payload)
   
#     response_object = {
#         "id": paramId,
#         "name": payload.name,
#         "date": payload.date,
#         "value" : payload.value,
#         "category" : payload.category,
#         "type" : payload.type,
#         "title" : payload.title
#     }
#     return response_object


# @router.get("/get/All", response_model=List[OperationHistoryDataDB])
# async def read_all_params():
#     return await crudParams.get_all_history_data()


# @router.get("/get/{date}", response_model=List[OperationHistoryDataDB])
# async def read_operation_history_data(date: str):
#     params = await crudParams.getOperationHistoryData(date)
#     if not params:
#         raise HTTPException(status_code=404, detail="Param not found")
#     return params


# #DELETE route
# @router.delete("/deleteFromId/{id}", response_model=OperationHistoryDataDB)
# async def delete_operation_history_data_id(id: int):
#     param = await crudParams.getOperationHistoryDataFromId(id)
#     if not param:
#         raise HTTPException(status_code=404, detail="item not found")
#     await crudParams.deleteHistoryDataFromId(id)

#     return param

# @router.delete("/delete/{date}", response_model=List[OperationHistoryDataDB])
# async def delete_operation_history_data_from_date(date : str):
#     return await crudParams.deleteHistoryDataFromDate(date)
