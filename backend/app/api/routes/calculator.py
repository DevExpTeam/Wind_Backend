import app.api.managers.user as user_manager
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
router = APIRouter()

@router.post("/test") 
def get_degradation_per_cycle(payload: CalculatorSchema):
    initial_cycle_data = payload.initial_cycle_data
    if initial_cycle_data is None:
        print('data is null')
        initial_cycle_data = [
		{
			"averageCyclesPerDay": 2.0,
			"retentionRate": [
				92.22, 88.58, 85.59, 83.04, 80.74, 78.63, 76.66,
				74.82, 73.08, 71.41, 69.79, 68.23, 66.71, 65.19,
				63.67, 62.15, 60.63, 59.11, 57.59, 56.07, 54.55,
				53.03, 51.51, 49.99, 48.47, 46.95, 45.43, 43.91,
				42.39, 40.87, 39.35, 37.83, 36.31, 34.79, 33.27,
				31.75, 30.23, 28.71, 27.19, 25.67, 24.15, 22.63,
				21.11, 19.59, 18.07,
			],
		},
		{
			"averageCyclesPerDay": 1.5,
			"retentionRate": [
				92.83, 89.56, 86.89, 84.61, 82.56, 80.68, 78.93,
				77.29, 75.75, 74.27, 72.83, 71.44, 70.09, 68.79,
				67.52, 66.28, 65.08, 63.88, 62.68, 61.48, 60.28,
				59.08, 57.88, 56.68, 55.48, 54.28, 53.08, 51.88,
				50.68, 49.48, 48.28, 47.08, 45.88, 44.68, 43.48,
				42.28, 41.08, 39.88, 38.68, 37.48, 36.28, 35.08,
				33.88, 32.68, 31.48,
			],
		},
		{
			"averageCyclesPerDay": 1.0,
			"retentionRate": [
				93.46, 90.59, 88.25, 86.27, 84.49, 82.85, 81.34,
				79.93, 78.6, 77.33, 76.08, 74.88, 73.72, 72.6, 71.5,
				70.44, 69.4, 68.38, 67.39, 66.41, 65.43, 64.45,
				63.47, 62.49, 61.51, 60.53, 59.55, 58.57, 57.59,
				56.61, 55.63, 54.65, 53.67, 52.69, 51.71, 50.73,
				49.75, 48.77, 47.79, 46.81, 45.83, 44.85, 43.87,
				42.89, 41.91,
			],
		},
	]
    if len(initial_cycle_data) != 3:
        return len(initial_cycle_data)
    ceiling_cycle = initial_cycle_data[0]['averageCyclesPerDay']
    middle_cycle = initial_cycle_data[1]['averageCyclesPerDay']
    floor_cycle = initial_cycle_data[2]['averageCyclesPerDay']

    ceiling_retention_rate = initial_cycle_data[0]['retentionRate']
    middle_retention_rate = initial_cycle_data[1]['retentionRate']
    floor_retention_rate = initial_cycle_data[2]['retentionRate']

    ceiling_degradation_per_cycle = []
    middle_degradation_per_cycle = []
    floor_degradation_per_cycle = []
    years = len(ceiling_retention_rate)

    for i in range(years):
        if i == 0:
            ceiling_degradation_per_cycle.append(100 - ceiling_retention_rate[i])
            middle_degradation_per_cycle.append(100 - middle_retention_rate[i])
            floor_degradation_per_cycle.append(100 - floor_retention_rate[i])
        else:
            ceiling_degradation_per_cycle.append(ceiling_retention_rate[i - 1] - ceiling_retention_rate[i])
            middle_degradation_per_cycle.append(middle_retention_rate[i - 1] - middle_retention_rate[i])
            floor_degradation_per_cycle.append(floor_retention_rate[i - 1] - floor_retention_rate[i])

    degradation_per_cycle_data = [
        {
            'averagePerCycle': ceiling_cycle,
            'degradationPerCycle': ceiling_degradation_per_cycle,
        },
        {
            'averagePerCycle': middle_cycle,
            'degradationPerCycle': middle_degradation_per_cycle,
        },
        {
            'averagePerCycle': floor_cycle,
            'degradationPerCycle': floor_degradation_per_cycle,
        },
    ]

    return degradation_per_cycle_data

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

