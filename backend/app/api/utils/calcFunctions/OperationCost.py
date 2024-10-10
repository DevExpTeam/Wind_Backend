from app.api.utils.calcFunctions.basicFun import multiplyArrayByNumber
from app.api.utils.calcFunctions.basicFun import multiplyArrays
from app.api.utils.calcFunctions.basicFun import sumArrays
from app.api.utils.calcFunctions.basicResults import calcInflationRate
import app.api.utils.calcFunctions.basicResults as basResult
import app.api.utils.calcFunctions.basicAssumptions as basInputs

inp = basInputs.basInputs

# Calculation of variable costs
global staffCostPerPeriod


staffCostPerPeriod = multiplyArrays(multiplyArrayByNumber(basResult.operation_periodFlag,inp.staff_cost_per_mwh["unitCost"] / inp.currency_unit),calcInflationRate(inp.staff_cost_per_mwh["inflationProfile"]),basResult.plantCapacityPerModelPeriod)
equipmentCostPerPeriod = multiplyArrays(multiplyArrayByNumber(basResult.operation_periodFlag,inp.equipment_cost_per_mwh["unitCost"] / inp.currency_unit),calcInflationRate(inp.equipment_cost_per_mwh["inflationProfile"]),basResult.plantCapacityPerModelPeriod)
consumablesCostPerPeriod = multiplyArrays(multiplyArrayByNumber(basResult.operation_periodFlag,inp.consumables_cost_per_mwh["unitCost"] / inp.currency_unit),calcInflationRate(inp.consumables_cost_per_mwh["inflationProfile"]),basResult.plantCapacityPerModelPeriod)
fuelCostPerPeriod = multiplyArrays(multiplyArrayByNumber(basResult.operation_periodFlag,inp.fuel_cost_per_mwh["unitCost"] / inp.currency_unit),calcInflationRate(inp.fuel_cost_per_mwh["inflationProfile"]),basResult.plantCapacityPerModelPeriod)
transportCostPerPeriod = multiplyArrays(multiplyArrayByNumber(basResult.operation_periodFlag,inp.transport_cost_per_mwh["unitCost"] / inp.currency_unit),calcInflationRate(inp.transport_cost_per_mwh["inflationProfile"]),basResult.plantCapacityPerModelPeriod)
maintenanceCostPerPeriod = multiplyArrays(multiplyArrayByNumber(basResult.operation_periodFlag,inp.maintenance_cost_per_mwh["unitCost"] / inp.currency_unit),calcInflationRate(inp.maintenance_cost_per_mwh["inflationProfile"]),basResult.plantCapacityPerModelPeriod)

totalVariableOAndMCost = sumArrays(staffCostPerPeriod,equipmentCostPerPeriod,consumablesCostPerPeriod,fuelCostPerPeriod, transportCostPerPeriod, maintenanceCostPerPeriod)


# Calculation of Fixed costs

spvCostsPerPeriod = multiplyArrayByNumber(multiplyArrays(basResult.operation_periodFlag,calcInflationRate(inp.spv_costs_per_year["inflationProfile"])),inp.spv_costs_per_year["fixedCost"] * inp.modelling_time_interval / 12)
insurancePerPeriod = multiplyArrayByNumber(multiplyArrays(basResult.operation_periodFlag,calcInflationRate(inp.insurance_per_year["inflationProfile"])),inp.insurance_per_year["fixedCost"] * inp.modelling_time_interval / 12)
landLeasePerPeriod = multiplyArrayByNumber(multiplyArrays(basResult.operation_periodFlag,calcInflationRate(inp.land_lease_per_year["inflationProfile"])),inp.land_lease_per_year["fixedCost"] * inp.modelling_time_interval / 12)
securityPerPeriod = multiplyArrayByNumber(multiplyArrays(basResult.operation_periodFlag,calcInflationRate(inp.security_per_year["inflationProfile"])),inp.security_per_year["fixedCost"] * inp.modelling_time_interval / 12)
communityPerPeriod = multiplyArrayByNumber(multiplyArrays(basResult.operation_periodFlag,calcInflationRate(inp.community_per_year["inflationProfile"])),inp.community_per_year["fixedCost"] * inp.modelling_time_interval / 12)
managementFeePerPeriod = multiplyArrayByNumber(multiplyArrays(basResult.operation_periodFlag,calcInflationRate(inp.management_fee_per_year["inflationProfile"])),inp.management_fee_per_year["fixedCost"] * inp.modelling_time_interval / 12)

totalFixedCost = sumArrays(spvCostsPerPeriod,insurancePerPeriod,landLeasePerPeriod,securityPerPeriod,communityPerPeriod,managementFeePerPeriod)

totalOperatingCost = sumArrays(totalFixedCost, totalVariableOAndMCost)