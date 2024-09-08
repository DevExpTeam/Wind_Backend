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
import json
router = APIRouter()

@router.post("/test") 
async def testFunc(parameter_id: int):
    data =  await parameter_manager.get_parameter_info_list_by_parameter_id(parameter_id)

    data= data[0]
    values = data["value"]

    construction_period_in_months = values["construction_period_in_months"]
    print(construction_period_in_months)
    return values
   

@router.post("/revenue/wholesale_day_ahead")
def get_wholesale_day_ahead(payload: WholeDaysAheadSchema): 
    modelStartDate = payload.modelStartDate
    operationStartDate = payload.operationStartDate

    decommissioningEndDate = payload.decommissioningEndDate
    assumptionsData = payload.assumptionsData
    revenueSetup = payload.revenueSetup
    detailedRevenueData = payload.detailedRevenueData 
    inflationInputs = payload.inflationInputs
    initialCycleData = payload.initialCycleData
    startingAssumptionsForBatteries = payload.startingAssumptionsForBatteries
    initialCapacity = payload.initialCapacity
    batteryDisposals = payload.batteryDisposals
    batteryEfficiency = payload.batteryEfficiency
    batteryAugmentation = payload.batteryAugmentation
    model = payload.model
    batteryDuration = payload.batteryDuration
    batteryCubes = payload.batteryCubes
    batteryExCubes = payload.batteryExCubes
    capexPaymentsProfile = payload.capexPaymentsProfile
    capexPaymentMilestones = payload.capexPaymentMilestones
    capexUEL = payload.capexUEL
    bessCapexForecast = payload.bessCapexForecast
    batterySensitivity = payload.batterySensitivity
    operationYears = payload.operationYears
    decommissioningEndDate = payload.decommissioningEndDate
    decommissioningStartDate = payload.decommissioningStartDate
    

    period = getMonthsNumberFromModelStartDate(modelStartDate, decommissioningEndDate) - 1

    selectedAssumptionsData = next((d for d in assumptionsData if d.get('providerName') == revenueSetup.get("forecastProviderChoice")), None).get("data")
    activeScenario = getActiveScenarioRevenueItems(revenueSetup,assumptionsData,startingAssumptionsForBatteries,detailedRevenueData)
    forecastProviderInputs = normalize_array_by_seasonality(
        round_array( multiply_number(next(
                (d for d in activeScenario if d.get('item') == "Wholesale Day Ahead Revenue"), None
                ).get("data"), 1/(1000 *((1 + selectedAssumptionsData.get("efficiency") / 100) / 2)))
               ,10), period)

    tempinflationAdjustmentFactor = round_array(calcInflationAdjustmentFactor(inflationInputs, selectedAssumptionsData.get("inflation"), selectedAssumptionsData.get("baseYear"), revenueSetup.get("inflation"), revenueSetup.get("baseYear")), 10)
    inflationAdjustmentFactor = normalize_array(annual_index_to_months(tempinflationAdjustmentFactor),period)

    operationsAsAPercentOfPeriod = get_as_a_percent_of_period(modelStartDate, operationStartDate, decommissioningStartDate, decommissioningEndDate)

    degradadedCapacityAdjustedForEffiAndAvailability = calcVintages(
        revenueSetup, 
        assumptionsData, 
        detailedRevenueData, 
        initialCycleData, 
        initialCapacity, 
        startingAssumptionsForBatteries, 
        batteryDisposals, 
        batteryEfficiency, 
        batteryAugmentation, 
        model, 
        batteryDuration, 
        batteryCubes, 
        batteryExCubes, 
        inflationInputs, 
        capexPaymentsProfile, 
        capexPaymentMilestones, 
        capexUEL, 
        bessCapexForecast, 
        batterySensitivity, 
        operationYears, 
        modelStartDate, 
        operationStartDate,
        decommissioningEndDate,
	decommissioningStartDate)
    return degradadedCapacityAdjustedForEffiAndAvailability
    degradadedCapacityAdjustedForEffiAndAvailability = round_array([d * 0.01 * startingAssumptionsForBatteries.batteryAvailability for d in calcVintages(revenueSetup, assumptionsData, detailedRevenueData, initialCycleData, initialCapacity, startingAssumptionsForBatteries, batteryDisposals, batteryEfficiency, batteryAugmentation, model, batteryDuration, batteryCubes, batteryExCubes, inflationInputs, capexPaymentsProfile, capexPaymentMilestones, capexUEL, bessCapexForecast, sensitivity, operationYears, modelStartDate, operationStartDate).totalGenerationCapacity], 10)
    
    
    return degradadedCapacityAdjustedForEffiAndAvailability

    return roundArray([d * forecastProviderInputs[index] * operationsAsAPercentOfPeriod[index] * inflationAdjustmentFactor[index] * (1 + revenueSensitivity) for index, d in enumerate(degradadedCapacityAdjustedForEffiAndAvailability)], 2)

