import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import app.api.utils.calcFunctions.basicAssumptions as inp
from app.api.utils.calcFunctions.basicFun import getDate

global calcPeriodsPerYear
calcPeriodsPerYear = int(12 / inp.modelling_time_interval)

global construction_start_dateTime
construction_start_dateTime = datetime.datetime.strptime(inp.construction_start_date,'%Y-%m-%d')

global calculation_period
calculation_period = int((inp.construction_period_in_months + inp.operation_period*12 + inp.decommissioning_period)/inp.modelling_time_interval) + 1

global constructionEndDate
constructionEndDate = getDate(inp.construction_start_date,inp.construction_period_in_months)+relativedelta(days=-1)

global commercialOperationDate
commercialOperationDate = constructionEndDate + relativedelta(days=+1)

global operationEndDate
operationEndDate = commercialOperationDate + relativedelta(years =+inp.operation_period) + relativedelta(days=-1)

global decommissioningEndDate
decommissioningEndDate = operationEndDate + relativedelta(months=+inp.decommissioning_period)

decommissioningStartDate = operationEndDate + relativedelta(days=+1)

global constructionDebtMaturityDate
constructionDebtMaturityDate = inp.construction_debt_assumption["repaymentStartDate"] + relativedelta(years =+ inp.construction_debt_assumption["constructionDebtTenure"]) + relativedelta(days=-1)

global dsraInitialFundingDate
dsraInitialFundingDate = inp.construction_debt_assumption["repaymentStartDate"] + relativedelta(months =- inp.modelling_time_interval)

def getPeriodFlag(flagStartDate,flagEndDate):
    flagResult = [0] * calculation_period
    tempDate = construction_start_dateTime
    tempIndex = 0
    while tempIndex < calculation_period: 
        if tempDate < flagStartDate:
            flagResult[tempIndex] = 0
        elif tempDate <= flagEndDate:
            flagResult[tempIndex] = 1
            tempDate <= flagStartDate
        else:
            flagResult[tempIndex] = 0
        tempIndex += 1
        tempDate = tempDate + relativedelta(months=+inp.modelling_time_interval)
    return flagResult

global operationStartDateFlag
operationStartDateFlag = getPeriodFlag(commercialOperationDate,commercialOperationDate)

global construction_period_flag
construction_period_flag = getPeriodFlag(construction_start_dateTime,constructionEndDate)

global operation_periodFlag
operation_periodFlag = getPeriodFlag(commercialOperationDate,operationEndDate)

global decommissioning_periodFlag
decommissioning_periodFlag = getPeriodFlag(decommissioningStartDate,decommissioningEndDate)

global constructionDebtTenureFlag
constructionDebtTenureFlag = getPeriodFlag(inp.construction_debt_assumption["repaymentStartDate"],constructionDebtMaturityDate)

global dsraInitialFundingDateFlag
dsraInitialFundingDateFlag = getPeriodFlag(dsraInitialFundingDate,dsraInitialFundingDate)

global operationEndDateFlag
operationEndDateFlag = getPeriodFlag(decommissioningStartDate + relativedelta(months=-inp.modelling_time_interval),decommissioningStartDate + relativedelta(days=-1))

global taxHolidayFlag
taxHolidayFlag = getPeriodFlag(commercialOperationDate, commercialOperationDate + relativedelta(years= + inp.income_tax_assumptions["taxHolidayPeriod"]) + relativedelta(days= -1))

def calcDaysInPeriod():
    daysResult = [0] * calculation_period
    hoursResult = [0] * calculation_period
    tempIndex = 0
    tempStartDate = construction_start_dateTime
    tempEndDate = construction_start_dateTime + relativedelta(months=+inp.modelling_time_interval)
    while tempIndex < calculation_period:
        daysResult[tempIndex] = (tempEndDate - tempStartDate).days
        hoursResult[tempIndex] = daysResult[tempIndex] *24
        tempIndex += 1
        tempStartDate = tempEndDate
        tempEndDate = tempEndDate + relativedelta(months=+inp.modelling_time_interval)
    return {"daysInPeriod":daysResult,
            "hoursInPeriod":hoursResult}

global daysInPeriod
daysInPeriod = calcDaysInPeriod()["daysInPeriod"]

global hoursInPeriod
hoursInPeriod = calcDaysInPeriod()["hoursInPeriod"]


global totalCapacity
totalCapacity = inp.capacity_per_turbine * inp.number_of_turbines

def calcCapacityFactor(factorData, factorPeriodData):
    
    capacityFactorStartDates = [commercialOperationDate] * (len(factorPeriodData)+1)
    i = 0
    tempStartDate = commercialOperationDate
    while i< len(factorPeriodData):
        capacityFactorStartDates[i+1] = tempStartDate + relativedelta(months=+factorPeriodData[i])
        tempStartDate =  capacityFactorStartDates[i+1]
        i+=1

    tempIndex = 0
    capacityFactorResult = [factorData[len(factorData)-1]] * calculation_period
    tempDate = construction_start_dateTime
    j = 0
    while j<len(capacityFactorStartDates):
        
        if j==0:
            while tempDate < capacityFactorStartDates[j]:
                capacityFactorResult[tempIndex] = 0
                tempDate = tempDate + relativedelta(months =+ inp.modelling_time_interval)
                tempIndex += 1
        else:
            while tempDate < capacityFactorStartDates[j]:
                capacityFactorResult[tempIndex] = factorData[j-1]
                tempDate = tempDate + relativedelta(months =+ inp.modelling_time_interval)
                tempIndex += 1

        j += 1

    return capacityFactorResult

global capacityFactor
capacityFactor = calcCapacityFactor(inp.capacity_factor_data,inp.capacity_factor_apply_period_data)

def calcPlantCapacityPerModelPeriod(capacityFactor,hoursPerPeriod):
    result = [0] * calculation_period
    i = 0

    while i<calculation_period:
        result[i] = round(capacityFactor[i] * hoursPerPeriod[i] * totalCapacity,2)
        i += 1

    return result

global plantCapacityPerModelPeriod
plantCapacityPerModelPeriod = calcPlantCapacityPerModelPeriod(capacityFactor,hoursInPeriod)


global indexationStartDate
indexationStartDate = commercialOperationDate + relativedelta(months=+12)

def calcInflationRate(inflation_rate_data):
    result = [1]*calculation_period
    compoundedInflationRate = [1] * calculation_period
    i = 0
    inflationRateLen = len(inflation_rate_data)
    while i < inflationRateLen:
        for j in range(calcPeriodsPerYear):
            compoundedInflationRate[i * calcPeriodsPerYear + j] = pow(1 + inflation_rate_data[i],inp.modelling_time_interval/12)-1
        i+= 1
    j = i * calcPeriodsPerYear
    while j<calculation_period:
        compoundedInflationRate[j] = compoundedInflationRate[j-1]
        j+=1
    inflationRateApplyingStartDate = construction_start_dateTime

    k = 0
    while k<calculation_period: 
        if inflationRateApplyingStartDate < indexationStartDate:
            result[k] = 1
        else:    
            result[k] = result[k-1] * (1 + compoundedInflationRate[k])
        inflationRateApplyingStartDate = inflationRateApplyingStartDate + relativedelta(months=+inp.modelling_time_interval)
        k+=1
    return result

# Assumptions sheet ~~~ 2 Construction Cost

global totalDevelopmentAndProject
global total_turbine_cost
global total_civil_work_expenditure
global total_logistics_and_others_expenditure
global total_developer_fee
global totalCapexSummaryAndPhasing
totalDevelopmentAndProject = (inp.development_and_consenting_service_per_mw + inp.environmental_surveys_per_mw + inp.resource_and_met_ocean_assessment_per_mw + inp.geological_and_hydrographical_surveys_per_mw + inp.engineering_and_consultancy) * totalCapacity
total_turbine_cost = inp.wind_turbine_cost_per_mw * totalCapacity
total_civil_work_expenditure = (inp.civil_work_Expenditure_per_mw + inp. balance_of_plant_expenditure_per_mw) * totalCapacity
total_logistics_and_others_expenditure = inp.logistics_and_others_expenditure_per_mw * totalCapacity
total_developer_fee = (totalDevelopmentAndProject + total_turbine_cost + total_civil_work_expenditure + total_logistics_and_others_expenditure) * inp.developer_fee_percentage/100
totalCapexSummaryAndPhasing = (totalDevelopmentAndProject + total_turbine_cost + total_civil_work_expenditure + total_logistics_and_others_expenditure + total_developer_fee)


global dsra_forward_periods
dsra_forward_periods = inp.dsra_years * 12 / inp.modelling_time_interval
