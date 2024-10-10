import app.api.utils.calcFunctions.basicResults as basResult
import app.api.utils.calcFunctions.basicAssumptions as basInputs
import app.api.utils.calcFunctions.ConstructionCost as consCosRes
from app.api.utils.calcFunctions.basicFun import calcSumOfValuesOfTheArray
from app.api.utils.calcFunctions.basicFun import sumArrays
from app.api.utils.calcFunctions.basicFun import multiplyArrayByNumber
from app.api.utils.calcFunctions.ConstructionCost import calcConsCostSummary
from app.api.utils.calcFunctions.ConstructionCost import calcDebtSummaryAccount
from app.api.utils.calcFunctions.ConstructionCost import calcVATonDevAndConsCostAndDeveloperFee
from app.api.utils.calcFunctions.ConstructionCost import calcDebtSummaryAccount

import app.api.utils.calcFunctions.Revenue as revResult
import app.api.utils.calcFunctions.OperationCost as operCostRes
import app.api.utils.calcFunctions.DecommissioningCost as decomCostRes
# Control accounts sheet ~~~ 1 Depreciation

inp = basInputs.basInputs
global depSummary

totalCapexData = calcConsCostSummary()
depSummary = {
    "startBalance" : [0] * basResult.calculation_period,
    "depPerPeriod" : [0] * basResult.calculation_period,
    "closingBalance" : [0] * basResult.calculation_period
    }

def calcDep(capexData, dep_years, periodFlag):

    period = len(capexData)
    depStartBalance = [0] * period
    depClosingBalance = [0] * period
    depPerPeriod = [0] * period

    totalCapexAmount = calcSumOfValuesOfTheArray(capexData)
    monthlyDepAmount = - totalCapexAmount * inp.modelling_time_interval / (dep_years * 12)
    index = 0
    
    while index < period:
        depPerPeriod[index] = monthlyDepAmount * periodFlag[index]
        depClosingBalance[index] = depStartBalance[index] + capexData[index] + depPerPeriod[index] * periodFlag[index]
        if index < period -1:
            depStartBalance[index + 1] = depClosingBalance[index]
        index += 1

    return {
        "startBalance" : depStartBalance,
        "depPerPeriod" : depPerPeriod,
        "closingBalance" : depClosingBalance
        }

def calcDepSummary():
    devAndProManagementDepResult = calcDep(consCosRes.dev_and_pro_management_per_period_for_dep, inp.dep_years["devAndProManagementYears"], basResult.operation_periodFlag)
    turbineCostDepResult = calcDep(consCosRes.turbine_cost_per_period_for_dep, inp.dep_years["turbineCostYears"], basResult.operation_periodFlag)
    civilWorkDepResult = calcDep(consCosRes.civil_work_per_period_for_dep, inp.dep_years["civilWorkYears"], basResult.operation_periodFlag)
    logisticsAndOthersDepResult = calcDep(consCosRes.logistics_and_others_per_period_for_dep, inp.dep_years["logisticsAndOthersYears"], basResult.operation_periodFlag)
    devFeeDepResult = calcDep(consCosRes.developer_fee_per_period_for_dep, inp.dep_years["developerFeeYears"], basResult.operation_periodFlag)

    depSummary["startBalance"] = sumArrays(devAndProManagementDepResult["startBalance"], turbineCostDepResult["startBalance"], civilWorkDepResult["startBalance"], logisticsAndOthersDepResult["startBalance"], devFeeDepResult["startBalance"])
    depSummary["depPerPeriod"] = sumArrays(devAndProManagementDepResult["depPerPeriod"], turbineCostDepResult["depPerPeriod"], civilWorkDepResult["depPerPeriod"], logisticsAndOthersDepResult["depPerPeriod"], devFeeDepResult["depPerPeriod"])
    depSummary["closingBalance"] = sumArrays(devAndProManagementDepResult["closingBalance"], turbineCostDepResult["closingBalance"], civilWorkDepResult["closingBalance"], logisticsAndOthersDepResult["closingBalance"], devFeeDepResult["closingBalance"])

    return depSummary

# Control accounts sheet ~~~ 2 Working Capital

def calcMovementInWorkingCapital(addtions,movementDays):
    startBalance = [0] * basResult.calculation_period
    cashMonthlyReceived = [0] * basResult.calculation_period
    cashNonMonthlyReceived = [0] * basResult.calculation_period
    lastPeriodAdjustment = [0] * basResult.calculation_period 
    closingBalance = [0] * basResult.calculation_period
    movementResult = [0] * basResult.calculation_period
    index = 0
    if inp.modelling_time_interval != 1:
        while index < basResult.calculation_period:
            cashNonMonthlyReceived[index] = min(addtions[index] * movementDays / basResult.daysInPeriod[index] - (startBalance[index] + addtions[index]), 0.0) * basResult.operation_periodFlag[index]
            lastPeriodAdjustment[index] = (startBalance[index] + addtions[index] + cashNonMonthlyReceived[index]) * (-basResult.operationEndDateFlag[index])
            closingBalance[index] = (startBalance[index] + addtions[index] + cashMonthlyReceived[index] + cashNonMonthlyReceived[index] + lastPeriodAdjustment[index])
            if index < basResult.calculation_period - 1:
                startBalance[index + 1] = closingBalance[index]
            index+=1
    else:
        while index < basResult.calculation_period:
            if index < int(movementDays / 30):
                cashMonthlyReceived[index] = 0
            else:
                cashMonthlyReceived[index] = -addtions[index-int(movementDays / 30)] * basResult.operation_periodFlag[index]
            lastPeriodAdjustment[index] = (startBalance[index] + addtions[index] + cashNonMonthlyReceived[index]) * (-basResult.operationEndDateFlag[index])
            closingBalance[index] = (startBalance[index] + addtions[index] + cashMonthlyReceived[index] + cashNonMonthlyReceived[index] + lastPeriodAdjustment[index])
            if index < basResult.calculation_period - 1:
                startBalance[index + 1] = closingBalance[index]
            index+=1
    movementResult = multiplyArrayByNumber(sumArrays(addtions, cashMonthlyReceived,cashNonMonthlyReceived), -1)
    movementResultForChange = sumArrays(movementResult, multiplyArrayByNumber(lastPeriodAdjustment ,-1))
# Collections is used for cash waterfall
    collections = multiplyArrayByNumber(sumArrays(lastPeriodAdjustment, cashMonthlyReceived,cashNonMonthlyReceived), -1)

    return {
        "startBalance" : startBalance,
        "closingBalance" : closingBalance,
        "movementResult" : movementResult,
        "collections" : collections,
        "movementResultForChange" : movementResultForChange
        }

# print(calcMovementInWorkingCapital(revResult.totalRevenue, inp.working_capital_days["receivableDays"])["movementResult"])
# print(calcMovementInWorkingCapital(operCostRes.totalOperatingCost, inp.working_capital_days["payableDays"]))


def calcEBIT():
    
    ebitda = sumArrays(revResult.totalRevenue, multiplyArrayByNumber(operCostRes.totalOperatingCost, -1))
    calcDepSummary()
    ebit =  sumArrays(ebitda, depSummary["depPerPeriod"])
    debtSummary = calcDebtSummaryAccount()
    pbt =  sumArrays(ebit, multiplyArrayByNumber(debtSummary["interest_accrued_per_period"], -1))
    
    return {
        "pbt" : pbt,
        "ebit" : ebit,
        "ebitda" : ebitda
        }
# Control accounts sheet ~~~ 3 Tax Calulation

# calcTax() function returns the items of the Income statement
def calcTax():
    pbtPerPeriod = calcEBIT()["pbt"]
    startBalance = [0] * basResult.calculation_period
    closingBalance = [0] * basResult.calculation_period
    taxLossPerPeriod = [0] * basResult.calculation_period
    utilizationOfHistoricalLosses = [0] * basResult.calculation_period
    profitForIncomeTax = [0] * basResult.calculation_period
    incomeTaxPerPeriod = [0] * basResult.calculation_period
    netIncomePerPeriod = [0] * basResult.calculation_period

    index = 0

    while index < basResult.calculation_period:
        if pbtPerPeriod[index] < 0:
            taxLossPerPeriod[index] = - pbtPerPeriod[index]
            utilizationOfHistoricalLosses[index] = 0
        else:
            taxLossPerPeriod[index] = 0
            utilizationOfHistoricalLosses[index] = - min(pbtPerPeriod[index], (startBalance[index] + taxLossPerPeriod[index]))
        closingBalance[index] = (startBalance[index] + taxLossPerPeriod[index] + utilizationOfHistoricalLosses[index])

        if basResult.taxHolidayFlag[index] == 1:
            profitForIncomeTax[index] = 0
        else:
            if closingBalance[index] > 0:
                profitForIncomeTax[index] = 0
            else:
                profitForIncomeTax[index] = pbtPerPeriod[index] + utilizationOfHistoricalLosses[index]
        if index < basResult.calculation_period - 1:
            startBalance[index + 1] = closingBalance[index] * basResult.operation_periodFlag[index + 1]

        incomeTaxPerPeriod[index] = profitForIncomeTax[index] * inp.income_tax_assumptions["incomeTaxRate"] / 100

        index += 1
    netIncomePerPeriod = sumArrays(pbtPerPeriod, multiplyArrayByNumber(incomeTaxPerPeriod, -1))
    return {
        "revenue" : revResult.totalRevenue,
        "electricitySoldRev" : revResult.revenueFromElectricitySale,
        "revFromFIT" : revResult.revenueFromFeedInTariff,
        "revFromMerchant" : revResult.revenueFromMerchant,
        "revenueFromOthers" : revResult.revenueForOthers,
        "totalOperatingCost" : multiplyArrayByNumber(operCostRes.totalOperatingCost, -1),
        "totalVariableCost" : multiplyArrayByNumber(operCostRes.totalVariableOAndMCost, -1),
        "totalFixedCost" : multiplyArrayByNumber(operCostRes.totalFixedCost, -1),
        "staffCost" : multiplyArrayByNumber(operCostRes.staffCostPerPeriod, -1),
        "equipmentCost" : multiplyArrayByNumber(operCostRes.equipmentCostPerPeriod, -1),
        "consumablesCost" : multiplyArrayByNumber(operCostRes.consumablesCostPerPeriod, -1),
        "fuelCost" : multiplyArrayByNumber(operCostRes.fuelCostPerPeriod, -1),
        "transportCost" : multiplyArrayByNumber(operCostRes.transportCostPerPeriod, -1),
        "maintenanceCost" : multiplyArrayByNumber(operCostRes.maintenanceCostPerPeriod, -1),
        "spvCost" : multiplyArrayByNumber(operCostRes.spvCostsPerPeriod, -1),
        "insruanaceCost" : multiplyArrayByNumber(operCostRes.insurancePerPeriod, -1),
        "landLeaseCost" : multiplyArrayByNumber(operCostRes.landLeasePerPeriod, -1),
        "securityCost" : multiplyArrayByNumber(operCostRes.securityPerPeriod, -1),
        "communityPaymentCost" : multiplyArrayByNumber(operCostRes.communityPerPeriod, -1),
        "managementFee" : multiplyArrayByNumber(operCostRes.managementFeePerPeriod, -1),
        "ebitda" : calcEBIT()["ebitda"],
        "depreciation" : depSummary["depPerPeriod"],
        "ebit" : calcEBIT()["ebit"],
        "interestExpense" :calcDebtSummaryAccount()["interest_accrued_per_period"],
        "pbt" : pbtPerPeriod,
        "tax" : multiplyArrayByNumber(incomeTaxPerPeriod, -1),
        "netIncome" : netIncomePerPeriod
        }


# 5 VAT Calculations

# 5.01 VAT During Operations ~~~ VAT on Revenue
def calcVATonRev(data):
    startBalance = [0] * basResult.calculation_period
    netAdditions = [0] * basResult.calculation_period
    monthlyCashSettlement = [0] * basResult.calculation_period
    nonMonthlyCashSettlement = [0] * basResult.calculation_period
    lastPeriodAdjustment = [0] * basResult.calculation_period
    closingBalance = [0] * basResult.calculation_period

    index = 0
    if inp.modelling_time_interval != 1:
        while index < basResult.calculation_period:
            netAdditions[index] = -data[index] * inp.vat_assumptions["vatOnRevenue"] / 100 * basResult.operation_periodFlag[index]
            nonMonthlyCashSettlement[index] = (netAdditions[index] * inp.vat_settlement_period / basResult.daysInPeriod[index] - (startBalance[index] + netAdditions[index]) * basResult.operation_periodFlag[index])
            lastPeriodAdjustment[index] = - basResult.operationEndDateFlag[index] * (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index])
            closingBalance[index] = (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index] + lastPeriodAdjustment[index])

            if index < basResult.calculation_period - 1:
                startBalance[index + 1] = closingBalance[index]
            index += 1

    else:
        while index < basResult.calculation_period:
            if index < int(inp.vat_settlement_period / 30):
                monthlyCashSettlement[index] = 0
            else:
                monthlyCashSettlement[index] = - netAdditions[index - int(inp.vat_settlement_period / 30)] * basResult.operation_periodFlag[index]
            netAdditions[index] = -data[index] * inp.vat_assumptions["vatOnRevenue"] / 100 * basResult.operation_periodFlag[index]
            lastPeriodAdjustment[index] = - basResult.operationEndDateFlag[index] * (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index])
            closingBalance[index] = (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index] + lastPeriodAdjustment[index])

            if index < basResult.calculation_period - 1:
                startBalance[index + 1] = closingBalance[index]
            index += 1

    return {
        "startBalance" : startBalance,
        "netAdditions" : netAdditions,
        "monthlyCashSettlement" : monthlyCashSettlement,
        "nonMonthlyCashSettlement" : nonMonthlyCashSettlement,
        "lastPeriodAdjustment" : lastPeriodAdjustment,
        "closingBalance" : closingBalance
        }

# 5.01 VAT During Operations ~~~ VAT on Revenue
def clacVATonCost(data):
    startBalance = [0] * basResult.calculation_period
    netAdditions = [0] * basResult.calculation_period
    monthlyCashSettlement = [0] * basResult.calculation_period
    nonMonthlyCashSettlement = [0] * basResult.calculation_period
    lastPeriodAdjustment = [0] * basResult.calculation_period
    closingBalance = [0] * basResult.calculation_period

    index = 0
    if inp.modelling_time_interval != 1:
        while index < basResult.calculation_period:
            netAdditions[index] = data[index] * inp.vat_assumptions["vatOnRevenue"] / 100 * basResult.operation_periodFlag[index]
            nonMonthlyCashSettlement[index] = (netAdditions[index] * inp.vat_settlement_period / basResult.daysInPeriod[index] - (startBalance[index] + netAdditions[index]) * basResult.operation_periodFlag[index])
            lastPeriodAdjustment[index] = - basResult.operationEndDateFlag[index] * (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index])
            closingBalance[index] = (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index] + lastPeriodAdjustment[index])

            if index < basResult.calculation_period - 1:
                startBalance[index + 1] = closingBalance[index]
            index += 1

    else:
        while index < basResult.calculation_period:
            if index < int(inp.vat_settlement_period / 30):
                monthlyCashSettlement[index] = 0
            else:
                monthlyCashSettlement[index] = - netAdditions[index - int(inp.vat_settlement_period / 30)] * basResult.operation_periodFlag[index]
            netAdditions[index] = data[index] * inp.vat_assumptions["vatOnRevenue"] / 100 * basResult.operation_periodFlag[index]
            lastPeriodAdjustment[index] = - basResult.operationEndDateFlag[index] * (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index])
            closingBalance[index] = (startBalance[index] + netAdditions[index] + monthlyCashSettlement[index] + nonMonthlyCashSettlement[index] + lastPeriodAdjustment[index])

            if index < basResult.calculation_period - 1:
                startBalance[index + 1] = closingBalance[index]
            index += 1

    return {
            "startBalance" : startBalance,
            "netAdditions" : netAdditions,
            "monthlyCashSettlement" : monthlyCashSettlement,
            "nonMonthlyCashSettlement" : nonMonthlyCashSettlement,
            "lastPeriodAdjustment" : lastPeriodAdjustment,
            "closingBalance" : closingBalance
            }

# 5.01 VAT During Operations ~~~ VAT summary
def calcVATsummary():
    vatOnRev = calcVATonRev(revResult.totalRevenue)
    vatOnCost = clacVATonCost(operCostRes.totalOperatingCost)
    startBalance = sumArrays(vatOnRev["startBalance"], vatOnCost["startBalance"])
    closingBalance = sumArrays(vatOnRev["closingBalance"], vatOnCost["closingBalance"])
    netAdditions = sumArrays(vatOnRev["netAdditions"], vatOnCost["netAdditions"])
    monthlyCashSettlement = sumArrays(vatOnRev["monthlyCashSettlement"], vatOnCost["monthlyCashSettlement"])
    nonMonthlyCashSettlement = sumArrays(vatOnRev["nonMonthlyCashSettlement"], vatOnCost["nonMonthlyCashSettlement"])
    lastPeriodAdjustment = sumArrays(vatOnRev["lastPeriodAdjustment"], vatOnCost["lastPeriodAdjustment"])

    movementResult = sumArrays(closingBalance, multiplyArrayByNumber(startBalance, -1))

    return {
            "startBalance" : startBalance,
            "netAdditions" : netAdditions,
            "monthlyCashSettlement" : monthlyCashSettlement,
            "nonMonthlyCashSettlement" : nonMonthlyCashSettlement,
            "lastPeriodAdjustment" : lastPeriodAdjustment,
            "closingBalance" : closingBalance,
            "movementResult" : movementResult
            }

def calcVATcarriedForwardFromConstructionToOperations():
    startBalance = [0] * basResult.calculation_period
    closingBalance = [0] * basResult.calculation_period
    vatPaid = [0] * basResult.calculation_period
    vatReceived = [0] * basResult.calculation_period
    lastPeriodAdjustment = [0] * basResult.calculation_period

    index = 0

    while index < basResult.calculation_period:
        vatReceived[index] = - startBalance[index] * basResult.operationStartDateFlag[index]
        lastPeriodAdjustment[index] = - basResult.operationEndDateFlag[index] * (startBalance[index] + vatPaid[index] + vatReceived[index])
        closingBalance[index] = (startBalance[index] + vatPaid[index] + vatReceived[index] + lastPeriodAdjustment[index])

        if index < basResult.calculation_period - 1:
            startBalance[index + 1] = closingBalance[index] + basResult.operationStartDateFlag[index + 1] * consCosRes.vat_summary_start_balance[index + 1]
        index += 1

    movementResult = sumArrays(closingBalance, multiplyArrayByNumber(startBalance, -1))
    
    return {
        "startBalance" : startBalance,
        "vatPaid" : vatPaid,
        "vatReceived" : vatReceived,
        "lastPeriodAdjustment" : lastPeriodAdjustment,
        "closingBalance" : closingBalance,
        "movementResult" : movementResult
        }

# Get the data of the CashFlow Statement items
def getIndirectCashFlowData():

# CF from Operations
    vatSummary = calcVATsummary()
    vatCarriedConsToOper = calcVATcarriedForwardFromConstructionToOperations()
    ebit = calcEBIT()["ebit"]
    depreciation = multiplyArrayByNumber(depSummary["depPerPeriod"], -1)
    changeInReceivables = calcMovementInWorkingCapital(revResult.totalRevenue, inp.working_capital_days["receivableDays"])["movementResultForChange"]
    changeInPayables = multiplyArrayByNumber(calcMovementInWorkingCapital(operCostRes.totalOperatingCost, inp.working_capital_days["payableDays"])["movementResultForChange"], -1)
    changeInVatDuringOperations = multiplyArrayByNumber(sumArrays(vatSummary["movementResult"], vatCarriedConsToOper["movementResult"] ), -1)
    taxPaid = calcTax()["tax"]
    decommissioningCost = multiplyArrayByNumber(decomCostRes.decommissioningCostPerPeriod, -1)

    cashflowFromOperations = sumArrays(ebit, depreciation, changeInPayables, changeInReceivables, changeInVatDuringOperations, taxPaid, decommissioningCost)

# CF from Investing
    constructionCapex = multiplyArrayByNumber(consCosRes.total_construction_cost_before_idc_and_fees, -1)
    interestDuringConsAndFees = multiplyArrayByNumber(sumArrays(consCosRes.interest_during_construction_per_period, consCosRes.arrangement_fee_per_period, consCosRes.commitment_fee_per_period), -1)
    dsraFunding = multiplyArrayByNumber(consCosRes.dsra_initial_funding_per_period, -1)
    vatOnConstruction = multiplyArrayByNumber(calcVATonDevAndConsCostAndDeveloperFee()["vat_summary_movement"], -1)

# CF from Financing
    bankDebtDrawdown = consCosRes.total_debt_per_period
    bankDebtRepayment = calcDebtSummaryAccount()["repayments_per_period"]
    bankDebtInterestPaid = calcDebtSummaryAccount()["interest_paid_per_period"]
    equityInvested = consCosRes.total_equity_per_period

    return {
        "ebit" : ebit,
        "depreciation" : depreciation,
        "changeInReceivables" : changeInReceivables,
        "changeInPayables" : changeInPayables,
        "changeInVatDuringOperations" : changeInVatDuringOperations,
        "taxPaid" : taxPaid,
        "decommissioningCost" : decommissioningCost,
        "cashflowFromOperations" : cashflowFromOperations,
        "constructionCapex" : constructionCapex,
        'interestDuringConsAndFees' : interestDuringConsAndFees,
        "dsraFunding" : dsraFunding,
        "vatOnConstruction" : vatOnConstruction,
        }

# print(getIndirectCashFlowData()["vatOnConstruction"])



# FS sheet ~~~ 4 Cash Waterfall

def getCashWaterfallItemsData():
    collections = calcMovementInWorkingCapital(revResult.totalRevenue,inp.working_capital_days["receivableDays"])["collections"]
    operationCostPaid = multiplyArrayByNumber(calcMovementInWorkingCapital(operCostRes.totalOperatingCost,inp.working_capital_days["payableDays"])["collections"], -1)
    decommissioningCost = multiplyArrayByNumber(decomCostRes.decommissioningCostPerPeriod, -1)
    taxPaid = calcTax()["tax"]
    vatDuringOperations = getIndirectCashFlowData()["changeInVatDuringOperations"]
    cashflowFromOpertaions = getIndirectCashFlowData()["cashflowFromOperations"]
    constructionCapex = multiplyArrayByNumber(consCosRes.total_construction_cost_before_idc_and_fees, -1)
    interestDuringConsAndFees = multiplyArrayByNumber(sumArrays(consCosRes.interest_during_construction_per_period, consCosRes.arrangement_fee_per_period, consCosRes.commitment_fee_per_period), -1)
    dsraFunding = multiplyArrayByNumber(consCosRes.dsra_initial_funding_per_period, -1)
    vatOnConstruction = multiplyArrayByNumber(calcVATonDevAndConsCostAndDeveloperFee()["vat_summary_movement"], -1)
    cashflowBeforeFunding = sumArrays(cashflowFromOpertaions, constructionCapex, interestDuringConsAndFees, dsraFunding, vatOnConstruction)
    equityInvested = multiplyArrayByNumber(consCosRes.total_debt_per_period, inp.equity_ratio / inp.debt_ratio)
    bankDebtDrawdown = consCosRes.total_debt_per_period
    cashflowAfterFunding = sumArrays(cashflowBeforeFunding, equityInvested, bankDebtDrawdown)
    cfads = cashflowAfterFunding
    bankDebtInterestPaid = calcDebtSummaryAccount()["interest_paid_per_period"]
    bankDebtRepayment = calcDebtSummaryAccount()["repayments_per_period"]
    cashflowBeforeDSRArelease = sumArrays(cfads, bankDebtInterestPaid, bankDebtRepayment)
    cashAvailableForEquityBeforeExcessDSRAcash = [0] * basResult.calculation_period
# Funding sheet ~~~ 1.36 DSRA calculation

    dsraStartBalance = [0] * basResult.calculation_period
    dsraClosingBalance = [0] * basResult.calculation_period
    fundsReleaseToMeetCFADSshortfall = [0] * basResult.calculation_period
    additionsToMaintainMinDSRAbalance = [0] * basResult.calculation_period
    excessFundsReleasedFromDSRA = [0] * basResult.calculation_period
    debtToBeServiced = multiplyArrayByNumber(consCosRes.debt_to_be_serviced_per_period, -1)
    cfadsShortfall = [0] * basResult.calculation_period
    targetDSRAbalance = [0] * basResult.calculation_period
    actualDSRAbalance = [0] * basResult.calculation_period
    excessFundsReleasedFromDSRAForCompare = [0] * basResult.calculation_period
    
    cashAvailableForEquityBeforeExcessDSRAcashForFundingSheet = [0] * basResult.calculation_period
    shortfallInDSRAfromMinimumBalance = [0] * basResult.calculation_period
    cashAvailableForDecommissioningReserve = [0] * basResult.calculation_period
# Control Accounts sheet ~~~ 4 Decommissioning Reserve

    decomReserveStartBalance = [0] * basResult.calculation_period
    decomReserveClosingBalance = [0] * basResult.calculation_period
    decomReserveAdditionsPerPeriod = [0] * basResult.calculation_period
    cashPaidPerPeriodForDecomReserve = multiplyArrayByNumber(decomCostRes.decommissioningCostPerPeriod, -1)
    wacc = (inp.equity_ratio * inp.cost_of_funds["costOfEquity"] / 100 + inp.debt_ratio * inp.cost_of_funds["costOfDebtPreTax"] / 100 * (1 - inp.income_tax_assumptions["incomeTaxRate"] / 100))
    discountRate = 1 / (1 + wacc / 100 * inp.modelling_time_interval / 12)
    totalDiscountPeriod = (inp.operation_period * 12 + inp.construction_period_in_months) / inp.modelling_time_interval
    pvOfDecommissioningReservePerPeriod = [0] * basResult.calculation_period
    cfadsAvailForDecomReservePerPeriod = [0] * basResult.calculation_period
    decomReserveForCF = [0] * basResult.calculation_period
    cashAvailableForEquityHolders = [0] * basResult.calculation_period




    index = 0
    while index < basResult.calculation_period:

        cfadsShortfall[index] = max(min(debtToBeServiced[index] + cfads[index], 0), 0)

        if index == 0:
            fundsReleaseToMeetCFADSshortfall[index] = max(cfadsShortfall[index] * basResult.constructionDebtTenureFlag[index], -(dsraStartBalance[index] - dsraFunding[index]))            
            targetDSRAbalance[index] = - (debtToBeServiced[index] + debtToBeServiced[index + 1]) * basResult.constructionDebtTenureFlag[index]
            actualDSRAbalance[index] = dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index]
            excessFundsReleasedFromDSRAForCompare[index] = max(actualDSRAbalance[index] - targetDSRAbalance[index], 0) * basResult.operation_periodFlag[index]
            cashAvailableForEquityBeforeExcessDSRAcash[index] = cashflowBeforeDSRArelease[index] - fundsReleaseToMeetCFADSshortfall[index]
            cashAvailableForEquityBeforeExcessDSRAcashForFundingSheet[index] = max(cashAvailableForEquityBeforeExcessDSRAcash[index], 0)
            shortfallInDSRAfromMinimumBalance[index] = - min(actualDSRAbalance[index] - targetDSRAbalance[index], 0)
            additionsToMaintainMinDSRAbalance[index] = min(cashAvailableForEquityBeforeExcessDSRAcashForFundingSheet[index], shortfallInDSRAfromMinimumBalance[index])
            if basResult.constructionDebtTenureFlag[index] == 1 and basResult.constructionDebtTenureFlag[index + 1] == 0:
                excessFundsReleasedFromDSRA[index] = -(dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index] + additionsToMaintainMinDSRAbalance[index])
            else:
                excessFundsReleasedFromDSRA[index] = - excessFundsReleasedFromDSRAForCompare[index]
            dsraClosingBalance[index] = dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index] + additionsToMaintainMinDSRAbalance[index] + excessFundsReleasedFromDSRA[index]
            cashAvailableForDecommissioningReserve[index] = max(cashAvailableForEquityBeforeExcessDSRAcash[index] - additionsToMaintainMinDSRAbalance[index] - excessFundsReleasedFromDSRA[index], 0)
            dsraStartBalance[index + 1] = dsraClosingBalance[index]
            pvOfDecommissioningReservePerPeriod[index] = basResult.operation_periodFlag[index] * inp.decommissioning_total_cost * pow(discountRate, totalDiscountPeriod - index - 1)
            cfadsAvailForDecomReservePerPeriod[index] = max(cashAvailableForDecommissioningReserve[index], 0)

            decomReserveAdditionsPerPeriod[index] = min(-pvOfDecommissioningReservePerPeriod[index] - decomReserveStartBalance[index], cfadsAvailForDecomReservePerPeriod[index])
            decomReserveClosingBalance[index] =  decomReserveStartBalance[index] + decomReserveAdditionsPerPeriod[index] + cashPaidPerPeriodForDecomReserve[index]
            decomReserveForCF[index] = decomReserveAdditionsPerPeriod[index] - cashPaidPerPeriodForDecomReserve[index]
            decomReserveStartBalance[index + 1] = decomReserveClosingBalance[index]

        elif index < basResult.calculation_period - 1:
            fundsReleaseToMeetCFADSshortfall[index] = cfadsShortfall[index] * basResult.constructionDebtTenureFlag[index]
            targetDSRAbalance[index] = - (debtToBeServiced[index] + debtToBeServiced[index + 1]) * basResult.constructionDebtTenureFlag[index]
            actualDSRAbalance[index] = dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index]
            excessFundsReleasedFromDSRAForCompare[index] = max(actualDSRAbalance[index] - targetDSRAbalance[index], 0) * basResult.operation_periodFlag[index]
            cashAvailableForEquityBeforeExcessDSRAcash[index] = cashflowBeforeDSRArelease[index] - fundsReleaseToMeetCFADSshortfall[index]
            cashAvailableForEquityBeforeExcessDSRAcashForFundingSheet[index] = max(cashAvailableForEquityBeforeExcessDSRAcash[index], 0)
            shortfallInDSRAfromMinimumBalance[index] = - min(actualDSRAbalance[index] - targetDSRAbalance[index], 0)
            additionsToMaintainMinDSRAbalance[index] = min(cashAvailableForEquityBeforeExcessDSRAcashForFundingSheet[index], shortfallInDSRAfromMinimumBalance[index])
            if basResult.constructionDebtTenureFlag[index] == 1 and basResult.constructionDebtTenureFlag[index + 1] == 0:
                excessFundsReleasedFromDSRA[index] = -(dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index] + additionsToMaintainMinDSRAbalance[index])
            else:
                excessFundsReleasedFromDSRA[index] = - excessFundsReleasedFromDSRAForCompare[index]
            dsraClosingBalance[index] = dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index] + additionsToMaintainMinDSRAbalance[index] + excessFundsReleasedFromDSRA[index]
            cashAvailableForDecommissioningReserve[index] = max(cashAvailableForEquityBeforeExcessDSRAcash[index] - additionsToMaintainMinDSRAbalance[index] - excessFundsReleasedFromDSRA[index], 0)
            dsraStartBalance[index + 1] = dsraClosingBalance[index]
            pvOfDecommissioningReservePerPeriod[index] = basResult.operation_periodFlag[index] * inp.decommissioning_total_cost * pow(discountRate, totalDiscountPeriod - index - 1)
            cfadsAvailForDecomReservePerPeriod[index] = max(cashAvailableForDecommissioningReserve[index], 0)

            decomReserveAdditionsPerPeriod[index] = min(-pvOfDecommissioningReservePerPeriod[index] - decomReserveStartBalance[index], cfadsAvailForDecomReservePerPeriod[index])
            decomReserveForCF[index] = decomReserveAdditionsPerPeriod[index] - cashPaidPerPeriodForDecomReserve[index]
            decomReserveClosingBalance[index] =  decomReserveStartBalance[index] + decomReserveAdditionsPerPeriod[index] + cashPaidPerPeriodForDecomReserve[index]
            decomReserveStartBalance[index + 1] = decomReserveClosingBalance[index]

        else:
            fundsReleaseToMeetCFADSshortfall[index] = cfadsShortfall[index] * basResult.constructionDebtTenureFlag[index]
            targetDSRAbalance[index] =  - debtToBeServiced[index]
            actualDSRAbalance[index] = dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index]
            excessFundsReleasedFromDSRAForCompare[index] = max(actualDSRAbalance[index] - targetDSRAbalance[index], 0) * basResult.operation_periodFlag[index]
            cashAvailableForEquityBeforeExcessDSRAcash[index] = cashflowBeforeDSRArelease[index] - fundsReleaseToMeetCFADSshortfall[index]
            cashAvailableForEquityBeforeExcessDSRAcashForFundingSheet[index] = max(cashAvailableForEquityBeforeExcessDSRAcash[index], 0)
            shortfallInDSRAfromMinimumBalance[index] = - min(actualDSRAbalance[index] - targetDSRAbalance[index], 0)
            additionsToMaintainMinDSRAbalance[index] = min(cashAvailableForEquityBeforeExcessDSRAcashForFundingSheet[index], shortfallInDSRAfromMinimumBalance[index])
            if basResult.constructionDebtTenureFlag[index] == 1 and basResult.constructionDebtTenureFlag[index + 1] == 0:
                excessFundsReleasedFromDSRA[index] = -(dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index] + additionsToMaintainMinDSRAbalance[index])
            else:
                excessFundsReleasedFromDSRA[index] = - excessFundsReleasedFromDSRAForCompare[index]
            cashAvailableForDecommissioningReserve[index] = max(cashAvailableForEquityBeforeExcessDSRAcash[index] - additionsToMaintainMinDSRAbalance[index] - excessFundsReleasedFromDSRA[index], 0)
            dsraClosingBalance[index] = dsraStartBalance[index] - dsraFunding[index] + fundsReleaseToMeetCFADSshortfall[index] + additionsToMaintainMinDSRAbalance[index] + excessFundsReleasedFromDSRA[index]
            pvOfDecommissioningReservePerPeriod[index] = basResult.operation_periodFlag[index] * inp.decommissioning_total_cost * pow(discountRate, totalDiscountPeriod - index - 1)
            cfadsAvailForDecomReservePerPeriod[index] = max(cashAvailableForDecommissioningReserve[index], 0)

            decomReserveAdditionsPerPeriod[index] = min(-pvOfDecommissioningReservePerPeriod[index] - decomReserveStartBalance[index], cfadsAvailForDecomReservePerPeriod[index])
            decomReserveForCF[index] = decomReserveAdditionsPerPeriod[index] - cashPaidPerPeriodForDecomReserve[index]
            decomReserveClosingBalance[index] =  decomReserveStartBalance[index] + decomReserveAdditionsPerPeriod[index] + cashPaidPerPeriodForDecomReserve[index]

        cashAvailableForEquityHolders[index] = cashAvailableForEquityBeforeExcessDSRAcash[index] - additionsToMaintainMinDSRAbalance[index] - excessFundsReleasedFromDSRA[index] + decomReserveForCF[index]
        index += 1

    return {
        "dsraClosingBalance" : dsraClosingBalance,
        "decomReserveClosingBalance" : decomReserveClosingBalance,
        "collections" : collections,
        "operationCostPaid" : operationCostPaid,
        "decommissioningCost" : decommissioningCost,
        "taxPaid" : taxPaid,
        "vatDuringOperations" : vatDuringOperations,
        "cashflowFromOpertaions" : cashflowFromOpertaions,
        "constructionCapex" : constructionCapex,
        "interestDuringConsAndFees" : interestDuringConsAndFees,
        "dsraFunding" : dsraFunding,
        "vatOnConstruction":getIndirectCashFlowData()["vatOnConstruction"],
        "cashflowBeforeFunding" : cashflowBeforeFunding,
        "equityInvested" : equityInvested,
        "bankDebtDrawdown" : bankDebtDrawdown,
        "cashflowAfterFunding" : cashflowAfterFunding,
        "cfads" : cfads,
        "bankDebtInterestPaid" : bankDebtInterestPaid,
        "bankDebtRepayment" : bankDebtRepayment,
        "cashflowBeforeDSRArelease" : cashflowBeforeDSRArelease,
        "fundsReleaseToMeetCFADSshortfall" : multiplyArrayByNumber(fundsReleaseToMeetCFADSshortfall, -1),
        "cashAvailableForEquityBeforeExcessDSRAcash" : cashAvailableForEquityBeforeExcessDSRAcash,
        "additionsToMaintainMinDSRAbalance" : multiplyArrayByNumber(additionsToMaintainMinDSRAbalance, -1),
        "excessFundsReleasedFromDSRA" : multiplyArrayByNumber(excessFundsReleasedFromDSRA, -1),
        "decommissioningReserve" : decomReserveForCF,
        "cashAvailableForEquityHolders" : cashAvailableForEquityHolders
        }
def getCashFlowData():
    value = getIndirectCashFlowData()
    val = getCashWaterfallItemsData()

    ebit = value["ebit"]
    depreciation = value["depreciation"]
    changeInReceivables = value['changeInReceivables']
    changeInPayables = value["changeInPayables"]
    changeInVatDuringOperations = value['changeInVatDuringOperations']
    taxPaid = value['taxPaid']
    decommissioningCost = value["decommissioningCost"]
    cashflowFromOperations = value["cashflowFromOperations"]
    constructionCapex = value["constructionCapex"]
    interestDuringConsAndFees = value["interestDuringConsAndFees"]
    dsraFunding = value["dsraFunding"]
    vatOnConstruction = value["vatOnConstruction"]
    decommissioningReserve = val["decommissioningReserve"]
    cashflowFromInvesting = sumArrays(constructionCapex, interestDuringConsAndFees, dsraFunding, vatOnConstruction, decommissioningReserve)
    bankDebtDrawdown = val["bankDebtDrawdown"]
    bankDebtRepayment = val["bankDebtRepayment"]
    bankDebtInterestPaid = val["bankDebtInterestPaid"]
    equityInvested = val["equityInvested"]
    dsra = sumArrays(val['fundsReleaseToMeetCFADSshortfall'], val["additionsToMaintainMinDSRAbalance"], val["excessFundsReleasedFromDSRA"])
    cashflowFromFinancing = sumArrays(bankDebtDrawdown, bankDebtRepayment, bankDebtInterestPaid, equityInvested, dsra)
    changeInCashDuringTheYear = sumArrays(cashflowFromOperations, cashflowFromInvesting, cashflowFromFinancing)
    closingCashBalance = [0] * basResult.calculation_period
    index = 0
    while index < basResult.calculation_period:
        if index == 0:
            closingCashBalance[index] = 0
        else:
            closingCashBalance[index] = changeInCashDuringTheYear[index] + closingCashBalance[index - 1]
        index += 1
    return {
    "ebit" : ebit,
    "depreciation" : depreciation,
    "changeInReceivables" : changeInReceivables,
    "changeInPayables" : changeInPayables,
    "changeInVatDuringOperations" : changeInVatDuringOperations,
    "taxPaid" : taxPaid,
    "decommissioningCost" : decommissioningCost,
    "cashflowFromOperations" : cashflowFromOperations,
    "constructionCapex" : constructionCapex,
    'interestDuringConsAndFees' : interestDuringConsAndFees,
    "dsraFunding" : dsraFunding,
    "vatOnConstruction" : vatOnConstruction,
    "decommissioningReserve" :decommissioningReserve,
    "cashflowFromInvesting" : cashflowFromInvesting,
    "bankDebtDrawdown" : bankDebtDrawdown,
    "bankDebtRepayment" : bankDebtRepayment,
    "bankDebtInterestPaid" : bankDebtInterestPaid,
    "equityInvested" : equityInvested,
    "dsra" : dsra,
    "cashflowFromFinancing" : cashflowFromFinancing,
    "closingCashBalance" : closingCashBalance,
    "changeInCashDuringTheYear" : changeInCashDuringTheYear
    }

# FS ~~~ 2 Balance Sheet

def calcBalanceSheet():
    
    cfData = getCashFlowData()
    cashAndEquivalents = cfData["closingCashBalance"]
    accountsReceiviables = calcMovementInWorkingCapital(revResult.totalRevenue, inp.working_capital_days["receivableDays"])["closingBalance"]
    vatReceivables = [0] * basResult.calculation_period

    vatSumClosingBalance = calcVATsummary()['closingBalance']
    vatCarriedForwardFromConsToOper = calcVATcarriedForwardFromConstructionToOperations()['closingBalance']
    vatSumOnConst = calcVATonDevAndConsCostAndDeveloperFee()["vat_summary_closing_balance"]

    index = 0
    while index < basResult.calculation_period:
        vatReceivables[index] = max(vatSumClosingBalance[index], 0 ) + max(vatSumOnConst[index], 0 ) + max(vatCarriedForwardFromConsToOper[index], 0 )
        index += 1

    totalCurrentAssets = sumArrays(cashAndEquivalents, accountsReceiviables, vatReceivables)
    calcDepSummary()
    fixedAssets = depSummary["closingBalance"]
    dsra = getCashWaterfallItemsData()["dsraClosingBalance"]
    decommissioningReserve = getCashWaterfallItemsData()["decomReserveClosingBalance"]
    totalNonCurrentAssets = sumArrays(fixedAssets, dsra, multiplyArrayByNumber(decommissioningReserve, -1))

    accountsPayables = calcMovementInWorkingCapital(operCostRes.totalOperatingCost, inp.working_capital_days["payableDays"])["closingBalance"]
    vatPayable = [0] * basResult.calculation_period
    bankDebt = calcDebtSummaryAccount()['closingBalace']
    totalNonCurrentLiabilites = bankDebt
    equityAdditions = sumArrays(consCosRes.money_raised_per_period, multiplyArrayByNumber(consCosRes.total_debt_per_period, -1))
    equityInvestedClosingBalance = [0] * basResult.calculation_period
    retainedEarnings = [0] * basResult.calculation_period
    netIncome = calcTax()['netIncome']

    i = 0
    while i < basResult.calculation_period:
        vatPayable[i] = - min(vatSumClosingBalance[i], 0 ) - min(vatSumOnConst[i], 0 ) - min(vatCarriedForwardFromConsToOper[i], 0 )
        if i == 0:
            equityInvestedClosingBalance[i] = equityAdditions[i]
            retainedEarnings[i] = netIncome[i]
        else:    
            equityInvestedClosingBalance[i] = equityInvestedClosingBalance[i - 1] + equityAdditions[i]
            retainedEarnings[i] = retainedEarnings[i - 1] + netIncome[i]
        i += 1

    totalCurrentLiabilites = sumArrays(accountsPayables, vatPayable)
    totalEquity = sumArrays(equityInvestedClosingBalance, retainedEarnings)
    
    return {
        "totalCurrentAssets" : totalCurrentAssets,
        "cashAndEquivalents" : cashAndEquivalents,
        "accountsReceiviables" : accountsReceiviables,
        "vatReceivables" : vatReceivables,
        "totalNonCurrentAssets" : totalNonCurrentAssets,
        "fixedAssets" : fixedAssets,
        "dsra" : dsra,
        "decommissioningReserve" : multiplyArrayByNumber(decommissioningReserve, -1),
        "accountsPayables" : accountsPayables,
        "vatPayable": vatPayable,
        "totalCurrentLiabilites" : totalCurrentLiabilites,
        'bankDebt' : bankDebt,
        "totalNonCurrentLiabilites" : totalNonCurrentLiabilites,
        "equityInvestedClosingBalance" : equityInvestedClosingBalance,
        "retainedEarnings" : retainedEarnings,
        "totalEquity" : totalEquity
        }