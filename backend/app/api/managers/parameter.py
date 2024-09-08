from app.api.model.parameterModel import *
from app.db import parameter, user, parameter_info, database
from datetime import datetime as dt
from fastapi import APIRouter, HTTPException, Path, status, Depends

from app.core.common import ErrorCode 

async def get_parameter_list_by_user_id(user_id: int): 
    params = await database.fetch_all(query=parameter.select().where(parameter.c.user_id == user_id))
    current_user = await database.fetch_one(query=user.select().where(user.c.id == user_id))
    return {"params": params, "param_setting": current_user.parameter_id}
    

# get full parameter with dict such as [{id, type, title, desc, data: parameter_info}, {}]
async def get_full_parameter_by_user_id(user_id: int):
    return 

# get full parameter with dict such as {cat1: {sub_cat1: val1, sub_cat2: val2}, cat2: {}}
async def get_parameter(parameter_id: int):
    return

async def create_parameter(payload: ParameterSchema, user_id):  
    existingParam = await database.fetch_one(query=parameter.select().where(payload.title == parameter.c.title and parameter.c.user_id == user_id))
    if existingParam:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail={
                "code": ErrorCode.PARAMTER_ALREADY_EXITS, 
                "message": "Alreay registered!"
             },
        )  
    insert_payload = {
        "user_id": payload.user_id, 
        "title": payload.title,
        "description": payload.description,
        "created_at": payload.created_at,
        "updated_at": payload.updated_at
    }
    try: 
        created_param_id = await database.execute(parameter.insert().values(insert_payload))  
        if payload.clone_id != -1:
            param_infos = await database.fetch_all(parameter_info.select().where(parameter_info.c.parameter_id == payload.clone_id))
            for param_info in param_infos:
                ins_payload = {
                    "parameter_id": created_param_id,
                    "param_index": param_info.param_index,
                    "value": param_info.value,
                    "created_at": payload.created_at,
                    "updated_at": payload.updated_at
                }
                await database.execute(parameter_info.insert().values(ins_payload))
        current_user = await database.fetch_one(query=user.select().where(payload.user_id == user.c.id))
        if current_user:
            update_value = created_param_id
            await database.execute(query=user.update().where(payload.user_id == user.c.id).values({"parameter_id": update_value}))
    except Exception as e:
        raise  
    params = await database.fetch_all(query=parameter.select().where(parameter.c.user_id == user_id))
    current_user = await database.fetch_one(query=user.select().where(user.c.id == user_id))
    return {"params": params, "param_setting": current_user.parameter_id}

async def delete_parameter(id,user_id):
    await database.execute(query=parameter.delete().where(parameter.c.id == id))
    await database.execute(query=parameter_info.delete().where(parameter_info.c.parameter_id == id))

    params = await database.fetch_all(query=parameter.select().where(parameter.c.user_id == user_id))
    if len(params) == 0:
        paramId = 0
        await database.execute(query = user.update().where(user.c.id == user_id).values({"parameter_id" : 0}))
    else:
        lastInputIndex = len(params)
        await database.execute(query = user.update().where(user.c.id == user_id).values({"parameter_id" : params[lastInputIndex - 1]["id"]}))
        current_user = await database.fetch_one(query=user.select().where(user.c.id == user_id))
        paramId = current_user.parameter_id
    return {"params": params, "param_setting": paramId}
 

 # async def deleteParamsFromTitle(title: str):
#     query = params.delete().where(title == params.c.title)
#     return await database.execute(query=query)

# async def getParamsFromId(id: int):
#     query = params.select().where(id == params.c.id)
#     return await database.fetch_one(query=query)

# async def deleteParamsFromId(id:int):
#     query = params.delete().where(id == params.c.id)
#     return await database.execute(query=query)



    
async def edit_parameter(id: int, payload: ParameterSchema, user_id): 
    try:  
        update_payload = {
            "user_id": payload.user_id,
            "title": payload.title,
            "description": payload.description, 
        }
        await database.execute(parameter.update().where(id == parameter.c.id).values(update_payload))  
        current_user = await database.fetch_one(query=user.select().where(payload.user_id == user.c.id))
    except Exception as e:
        raise   
    params = await database.fetch_all(query=parameter.select().where(parameter.c.user_id == user_id))
    current_user = await database.fetch_one(query=user.select().where(user.c.id == user_id))
    return {"params": params, "param_setting": current_user.parameter_id} 

# async def delete_parameter(id: int):
#     return

async def get_parameter_info_list_by_parameter_id(parameter_id: int):
    param_infos = await database.fetch_all(query=parameter_info.select().where(parameter_id==parameter_info.c.parameter_id))
    return param_infos 

async def create_or_update_parameter_info(payload: ParameterInfoSchema): 
    existingParam = await database.fetch_one(query=parameter_info.select().where(payload.param_index == parameter_info.c.param_index).where(payload.parameter_id==parameter_info.c.parameter_id))
    if not existingParam: 
        insert_payload = {
            "parameter_id": payload.parameter_id,
            "param_index": payload.param_index,
            "value": payload.value,
            "created_at": payload.created_at,
            "updated_at": payload.updated_at
        }
        try: 
            created_param_id = await database.execute(parameter_info.insert().values(insert_payload))  
        except Exception as e:
            raise  
    else:
        update_payload = {
            "parameter_id": payload.parameter_id,
            "param_index": payload.param_index,
            "value": payload.value,
            "created_at": payload.created_at,
            "updated_at": payload.updated_at
        }
        try: 
            await database.execute(parameter_info.update().where(existingParam.id == parameter_info.c.id).values(update_payload))  
        except Exception as e:
            raise 
    param_infos = await database.fetch_all(query=parameter_info.select().where(payload.parameter_id==parameter_info.c.parameter_id))
    return param_infos 

async def edit_parameter_info(id: int, payload: ParameterInfoSchema):
    update_payload = {
        "parameter_id": payload.parameter_id,
        "param_index": payload.param_index,
        "value": payload.value, 
    } 
    try: 
        await database.execute(parameter_info.update().where(id == parameter_info.c.id).values(update_payload))  
    except Exception as e:
        raise  
    param_infos = await database.fetch_all(query=parameter_info.select().where(payload.parameter_id==parameter_info.c.parameter_id))
    return param_infos  

# async def delete_parameter_info(id: int):
#     return
 
# async def post(payload: ParameterSchema):
#     created_date = dt.now().strftime("%Y-%m-%d %H:%M")
#     updated_date = dt.now().strftime("%Y-%m-%d %H:%M")

    
#     query = params.select().where(payload.title == params.c.title)
#     res = await database.fetch_all(query=query)

#     #In case the param is not exists

#     if not res:
#         query = params.insert().values(
#             title=payload.title, 
#             user = payload.user,
#             category=payload.category, 
#             value =payload.value, 
#             type = payload.type,
#             unit = payload.unit, 
#             created_date=created_date,
#             updated_date = updated_date
#         )
#         return await database.execute(query=query)

#     # In case the param is already exists

#     updated_date = dt.now().strftime("%Y-%m-%d %H:%M")
#     query = (
#         params.update().where(payload.title == params.c.title).values(title=payload.title, 
#         value= payload.value,   type = payload.type , category=payload.category, user = payload.user, unit = payload.unit, updated_date = updated_date)
#         .returning(params.c.id)
#     )
#     return await database.execute(query=query)

# async def get_all():
#     query = params.select()
#     res = await database.fetch_all(query=query)
#     print(res)
#     return res

# async def getParamsFromCategory(category: str):
#     query = params.select().where(category == params.c.category)
#     return await database.fetch_all(query=query)

# async def getParamsFromTitle(title: str):
#     query = params.select().where(title == params.c.title)
#     return await database.fetch_one(query=query)

# async def deleteParamsFromTitle(title: str):
#     query = params.delete().where(title == params.c.title)
#     return await database.execute(query=query)

# async def getParamsFromId(id: int):
#     query = params.select().where(id == params.c.id)
#     return await database.fetch_one(query=query)

# async def deleteParamsFromId(id:int):
#     query = params.delete().where(id == params.c.id)
#     return await database.execute(query=query)





# async def postOperationHistoryList(payload: OperationHistoryListDB):

#     query = operationHistoryList.select().where( payload.date == operationHistoryList.c.date)
#     res = await database.fetch_all(query=query)

#     #In case the param is not exists

#     if not res:
#         query = operationHistoryList.insert().values(
#             date=payload.date, 
#             name = payload.name
#         )
#         return await database.execute(query=query)

#     return await database.execute(query=query)


# async def get_all_history_lists():
#     query = operationHistoryList.select()
#     return await database.fetch_all(query=query)

# async def getOperationHistoryListFromId(id):
#     query = operationHistoryList.select().where(id == operationHistoryList.c.id)
#     return await database.fetch_one(query=query)

# async def deleteOperationHistoryList(date: str):
#     query = operationHistoryList.delete().where(date == operationHistoryList.c.date)
#     return await database.execute(query=query)

# async def deleteHistoryListFromId(id):
#     query = operationHistoryList.delete().where(id == operationHistoryList.c.id)
#     return await database.execute(query=query)




# async def postOperationHistoryData(payload: OperationHistoryDataDB):
  

#         query = operationHistoryData.insert().values(
#             date=payload.date, 
#             name = payload.name,
#             value =payload.value,
#             category = payload.category,
#             title = payload.title,
#             type = payload.type,
#         )
#         return await database.execute(query=query)

#     # In case the param is already exists

    

# async def get_all_history_data():
#     query = operationHistoryData.select()
#     return await database.fetch_all(query=query)

# async def getOperationHistoryData(date: str):
#     query = operationHistoryData.select().where(date == operationHistoryData.c.date)
#     return await database.fetch_all(query=query)

# async def getOperationHistoryDataFromId(id):
#     query = operationHistoryData.select().where(id == operationHistoryData.c.id)
#     return await database.fetch_one(query=query)


# async def deleteHistoryDataFromDate(date: str):
#     query = operationHistoryData.delete().where(date == operationHistoryData.c.date)
#     return await database.execute(query=query)

# async def deleteHistoryDataFromId(id):
#     query = operationHistoryData.delete().where(id == operationHistoryData.c.id)
#     return await database.execute(query=query)

