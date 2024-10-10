import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from app.api.utils.calcFunctions.basicFun import sumArrays
from app.api.utils.calcFunctions.basicFun import multiplyArrayByNumber
from app.api.utils.calcFunctions.basicFun import multiplyArrays
from app.api.utils.calcFunctions.basicFun import getDate

from app.api.utils.calcFunctions.basicResults import getPeriodFlag
from app.api.utils.calcFunctions.basicResults import calcInflationRate
import app.api.utils.calcFunctions.basicAssumptions as basInputs
import app.api.utils.calcFunctions.basicResults as basResult

inp = basInputs.basInputs

def calcIndexedResult(inflation_rate_data, baseValue):
    
    indexedResult = [0] * basResult.calculation_period
    indexValues = calcInflationRate(inflation_rate_data)
    i=0
    while i < basResult.calculation_period:
        indexedResult[i] = indexValues[i] * baseValue * basResult.operation_periodFlag[i]
        i += 1
    return indexedResult

global feedInTariffAfterInflation
feedInTariffAfterInflation = calcIndexedResult(inp.feed_in_tariff_price_per_mw["inflationProfile"],inp.feed_in_tariff_price_per_mw["unitCost"])
global merchantPriceAfterInflation
merchantPriceAfterInflation = calcIndexedResult(inp.merchant_price_per_mwh["inflationProfile"],inp.merchant_price_per_mwh["unitCost"])

global ppaStartDate
ppaStartDate = basResult.commercialOperationDate

global ppaEndDate
ppaEndDate = ppaStartDate + relativedelta(years=+inp.ppaTerm) + relativedelta(days=-1)

global ppaTermFlag
ppaTermFlag = getPeriodFlag(ppaStartDate,ppaEndDate)


def calcElectricitySoldPercentage():
    tempPeriodStartDate = basResult.construction_start_dateTime
    i = 0
    percentageValuesOfFIT = [inp.electricity_sold_percentage_during_ppa_term] * basResult.calculation_period
    percentageValuesOfMerchant = [1-inp.electricity_sold_percentage_during_ppa_term] * basResult.calculation_period
    while i < basResult.calculation_period:
        if tempPeriodStartDate < ppaStartDate:
            percentageValuesOfFIT[i] = 0
            percentageValuesOfMerchant[i] = 1 - percentageValuesOfFIT[i] 
        elif tempPeriodStartDate < ppaEndDate:
            percentageValuesOfFIT[i] = inp.electricity_sold_percentage_during_ppa_term
            percentageValuesOfMerchant[i] = 1 - percentageValuesOfFIT[i] 
        else:
            percentageValuesOfFIT[i] = 0
            percentageValuesOfMerchant[i] = 1 - percentageValuesOfFIT[i] 

        tempPeriodStartDate = tempPeriodStartDate + relativedelta(months=+ inp.modelling_time_interval)
        i+=1
    percentageValuesOfMerchant[basResult.calculation_period-1] = 0
    percentageValuesOfFIT[basResult.calculation_period-1] = 0
    return {"percentageValuesOfFIT":percentageValuesOfFIT,"percentageValuesOfMerchant":percentageValuesOfMerchant}

global electricitySoldPercentage
electricitySoldPercentage = calcElectricitySoldPercentage()
    

def revenueFromFIT(electricitySoldPercentage,plantCapacityPerModelPeriod,feedInTariffAfterInflation):
    revenueOfFIT = [0] * basResult.calculation_period
    i=0
    while i < basResult.calculation_period:
        revenueOfFIT[i] = electricitySoldPercentage["percentageValuesOfFIT"][i] * feedInTariffAfterInflation[i] * plantCapacityPerModelPeriod[i]/inp.currency_unit
        i+=1
    return revenueOfFIT

global revenueFromFeedInTariff
revenueFromFeedInTariff = revenueFromFIT(electricitySoldPercentage,basResult.plantCapacityPerModelPeriod,feedInTariffAfterInflation)

def revenueFromMerchantPrice(electricitySoldPercentage,plantCapacityPerModelPeriod,merchantPriceAfterInflation):
    revenueOfFIT = [0] * basResult.calculation_period
    i=0
    while i < basResult.calculation_period:
        revenueOfFIT[i] = electricitySoldPercentage["percentageValuesOfMerchant"][i] * merchantPriceAfterInflation[i] * plantCapacityPerModelPeriod[i]/inp.currency_unit
        i+=1
    return revenueOfFIT

global revenueFromMerchant
revenueFromMerchant = revenueFromMerchantPrice(electricitySoldPercentage,basResult.plantCapacityPerModelPeriod,merchantPriceAfterInflation)

global revenueFromElectricitySale
revenueFromElectricitySale = sumArrays(revenueFromFeedInTariff,revenueFromMerchant)

global revenueForOthers
revenueForOthers = multiplyArrayByNumber(multiplyArrays(basResult.operation_periodFlag, calcInflationRate(inp.revenue_from_others_per_month["inflationProfile"])),inp.modelling_time_interval * inp.revenue_from_others_per_month["unitCost"] / inp.currency_unit)

global totalRevenue
totalRevenue = sumArrays(revenueFromElectricitySale,revenueForOthers)
