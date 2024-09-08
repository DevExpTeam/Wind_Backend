# import app.api.cruds.inputParams as crudParams
# from app.api.model.inputParamsModel import  OperationHistoryListDB, OperationHistoryListSchema
# from fastapi import APIRouter, HTTPException, Path
# from typing import List 
# from datetime import datetime as dt
# router = APIRouter()


# #This is for the history list when the user save the status



# # These are api routes for history lists
# @router.post("/", response_model=OperationHistoryListDB, status_code=201)
# async def create_new_history_lists(payload: OperationHistoryListSchema):
#     print(payload)
#     paramId = await crudParams.postOperationHistoryList(payload)
   
#     response_object = {
#         "id": paramId,
#         "name": payload.name,
#         "date": payload.date,
#     }
#     return response_object


# @router.get("/get/All", response_model=List[OperationHistoryListDB])
# async def read_all_params():
#     return await crudParams.get_all_history_lists()

# #DELETE route
# @router.delete("/deleteFromId/{id}", response_model=OperationHistoryListDB)
# async def delete_history_list_from_id(id: int):
#     param = await crudParams.getOperationHistoryListFromId(id)
#     if not param:
#         raise HTTPException(status_code=404, detail="item not found")
#     await crudParams.deleteHistoryListFromId(id)
#     return param
