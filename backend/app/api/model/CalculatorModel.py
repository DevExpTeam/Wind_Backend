from pydantic import BaseModel, Field, NonNegativeInt, EmailStr
from datetime import datetime as dt
from pytz import timezone as tz
from typing import Optional

class CalculatorSchema(BaseModel): 
    initial_cycle_data: list = []
 
    class Config:  
        json_schema_extra={
            "example": {
            }
        } 


class WholeDaysAheadSchema(BaseModel):  
    decommissioningStartDate:str
    decommissioningEndDate: str
    modelStartDate: str  
    assumptionsData: list = []
    revenueSetup: dict
    startingAssumptionsForBatteries: dict
    detailedRevenueData: list
    inflationInputs: list
    operationStartDate:str
   
    initialCycleData:list
    startingAssumptionsForBatteries:dict
    initialCapacity:int
    batteryDisposals:dict
    batteryEfficiency:dict
    batteryAugmentation:dict
    model :str
    batteryDuration:int
    batteryCubes:dict
    batteryExCubes:dict
    capexPaymentsProfile:list
    capexPaymentMilestones:list
    capexUEL:list
    bessCapexForecast:dict
    batterySensitivity:float
    operationYears:int


    class Config:  
        json_schema_extra={
            "example": {
                "model": "Bringa"
            }
        } 

