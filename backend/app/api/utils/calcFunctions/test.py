import app.api.utils.calcFunctions.basicAssumptions as basInputs
import app.api.utils.calcFunctions.Revenue as rev
import app.api.utils.calcFunctions.OperationCost as operCost
import app.api.utils.calcFunctions.basicResults as basResult
import app.api.utils.calcFunctions.ConstructionCost as consCost
from app.api.utils.calcFunctions.basicFun import multiplyArrayByNumber
from app.api.utils.calcFunctions.ControlAccounts import calcDepSummary
from app.api.utils.calcFunctions.ConstructionCost import calcVATonDevAndConsCostAndDeveloperFee
import app.api.utils.calcFunctions.basicAssumptions as inp
import app.api.utils.calcFunctions.ControlAccounts as controlAccountsRes

from app.api.utils.calcFunctions.ConstructionCost import calcDebtSummaryAccount
from app.api.utils.calcFunctions.ControlAccounts import getCashWaterfallItemsData
from app.api.utils.calcFunctions.ControlAccounts import getCashFlowData
from app.api.utils.calcFunctions.ControlAccounts import calcTax
from app.api.utils.calcFunctions.ControlAccounts import calcBalanceSheet





def waterfallReturn():
    return getCashWaterfallItemsData()
def cashflowReturn():
    return getCashFlowData()
def profitAndLossReturn():
    return calcTax()
def balanceSheetReturn():
    return calcBalanceSheet()
def revenueGraphReturn():
    graphData = {
        "totalRevenue" : rev.totalRevenue,
        "electricitySoldRev" : rev.revenueFromElectricitySale,
        "revFromFIT" : rev.revenueFromFeedInTariff,
        "revFromMerchant" : rev.revenueFromMerchant,
        "revenueFromOthers" : rev.revenueForOthers,
            }
    return graphData

def costGraphReturn():
    graphData = {
        "totalOperatingCost" : multiplyArrayByNumber(operCost.totalOperatingCost, -1),
        "totalVariableCost" : multiplyArrayByNumber(operCost.totalVariableOAndMCost, -1),
        "totalFixedCost" : multiplyArrayByNumber(operCost.totalFixedCost, -1),
        "staffCost" : multiplyArrayByNumber(operCost.staffCostPerPeriod, -1),
        "equipmentCost" : multiplyArrayByNumber(operCost.equipmentCostPerPeriod, -1),
        "consumablesCost" : multiplyArrayByNumber(operCost.consumablesCostPerPeriod, -1),
        "fuelCost" : multiplyArrayByNumber(operCost.fuelCostPerPeriod, -1),
        "transportCost" : multiplyArrayByNumber(operCost.transportCostPerPeriod, -1),
        "maintenanceCost" : multiplyArrayByNumber(operCost.maintenanceCostPerPeriod, -1),
        "spvCost" : multiplyArrayByNumber(operCost.spvCostsPerPeriod, -1),
        "insruanaceCost" : multiplyArrayByNumber(operCost.insurancePerPeriod, -1),
        "landLeaseCost" : multiplyArrayByNumber(operCost.landLeasePerPeriod, -1),
        "securityCost" : multiplyArrayByNumber(operCost.securityPerPeriod, -1),
        "communityPaymentCost" : multiplyArrayByNumber(operCost.communityPerPeriod, -1),
        "managementFee" : multiplyArrayByNumber(operCost.managementFeePerPeriod, -1),
            }
    return graphData