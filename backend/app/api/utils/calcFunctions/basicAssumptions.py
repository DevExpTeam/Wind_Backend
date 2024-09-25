import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import os
import json

import app.api.utils.calcFunctions.input as val
from app.api.utils.calcFunctions.input import dbInput

values = []
global currency_unit
currency_unit = 1000

# Timing assumptions
global modelling_time_interval
modelling_time_interval = 6
global construction_start_date
construction_start_date = "2021-01-01"

global construction_period_in_months
construction_period_in_months = 24

global operation_period
operation_period = 40

global decommissioning_period
decommissioning_period = 3


# Turibine assumptions

global capacity_per_turbine
capacity_per_turbine = 3

global number_of_turbines
number_of_turbines = 20

global capacity_factor_data
capacity_factor_data = [0.25,0.27,0.29,0.3,0.32]

global capacity_factor_apply_period_data
capacity_factor_apply_period_data = [12,18,18,20]

# Indexation assumptions

global inflation_rate_data
inflation_rate_data = [0.020,0.020,0.025,0.025,0.0275,0.0275,0.030,0.030,0.030,0.030]

global inflation_base_year
inflation_base_year = 2021

# Revenue assumptions

global feed_in_tariff_price_per_mw
feed_in_tariff_price_per_mw = {"unitCost":110,"inflationProfile":inflation_rate_data}

global merchant_price_per_mwh
merchant_price_per_mwh = {"unitCost":40,"inflationProfile":inflation_rate_data}

global revenue_from_others_per_month
revenue_from_others_per_month = {"unitCost":25000,"inflationProfile":inflation_rate_data}

global ppaTerm
ppaTerm = 15

global electricity_sold_percentage_during_ppa_term
electricity_sold_percentage_during_ppa_term = 0.8

# Variable O&M Cost Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.01

global staff_cost_per_mwh
global equipment_cost_per_mwh
global consumables_cost_per_mwh
global fuel_cost_per_mwh
global transport_cost_per_mwh
global maintenance_cost_per_mwh

staff_cost_per_mwh = {"unitCost":10,"inflationProfile":inflation_rate_data}
equipment_cost_per_mwh = {"unitCost":3,"inflationProfile":inflation_rate_data}
consumables_cost_per_mwh = {"unitCost":1,"inflationProfile":inflation_rate_data}
fuel_cost_per_mwh = {"unitCost":1,"inflationProfile":inflation_rate_data}
transport_cost_per_mwh = {"unitCost":3,"inflationProfile":inflation_rate_data}
maintenance_cost_per_mwh = {"unitCost":3,"inflationProfile":inflation_rate_data}

# Other Fixed Costs Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.02
# unit of fixed costs is 1000
global spv_costs_per_year
global insurance_per_year
global land_lease_per_year
global security_per_year
global community_per_year
global management_fee_per_year

spv_costs_per_year = {"fixedCost":400,"inflationProfile":inflation_rate_data}
insurance_per_year = {"fixedCost":219.2,"inflationProfile":inflation_rate_data}
land_lease_per_year = {"fixedCost":8.5,"inflationProfile":inflation_rate_data}
security_per_year = {"fixedCost":200,"inflationProfile":inflation_rate_data}
community_per_year = {"fixedCost":45,"inflationProfile":inflation_rate_data}
management_fee_per_year = {"fixedCost":8.5,"inflationProfile":inflation_rate_data}

# Construction cost assumption ~~~ Assumptions sheet/2 Construction Cost
# Development and Project Management
development_and_consenting_service_per_mw = 50
environmental_surveys_per_mw = 5.15
resource_and_met_ocean_assessment_per_mw = 5.15
geological_and_hydrographical_surveys_per_mw = 5.15
engineering_and_consultancy = 5.15

# Turbine Cost
wind_turbine_cost_per_mw = 500

# Civil Work
civil_work_Expenditure_per_mw = 350
balance_of_plant_expenditure_per_mw = 300

# Logistics and Others
logistics_and_others_expenditure_per_mw = 0

# Developer's Fee
developer_fee_percentage = 1

# Capex Phasing

capex_phasing_data = {
    "developmentAndProjectManagement":[50,50,0,0],
    "turbineCost":[0,35,35,30],
    "civilWork":[0,35,35,30],
    "logisticsAndOthers":[0,35,35,30],
    "developerFee":[0,100,0,0]
}


decommissioning_total_cost = 1000

# 6 Financing Assumptions

# 6.01 Debt Equity Ratio
debt_ratio = 75
equity_ratio = 100 - debt_ratio

# 6.03 Construction Debt Assumptions

construction_debt_assumption = {
    "constructionDebtTenure" : 20, 
    "repaymentStartDate" : datetime.datetime.strptime(construction_start_date,'%Y-%m-%d') + relativedelta(months=+construction_period_in_months),
    "libor":3,
    "margin":3,
    "dscr" : 1.5
    }

# 6.07 Fees
fees_assumption = {
    "arrangementFeesPercentage" : 0.3,
    "commitmentFeesPercentage" : 0.3
    }
# 6.08 DSRA
dsra_years = 1

# 7 Other Assumptions

working_capital_days = {
    "receivableDays" : 60,
    "payableDays" : 60
    }
income_tax_assumptions = {
    "incomeTaxRate" : 20,
    "taxHoliday" : 0,
    "taxHolidayPeriod" :2
    }
vat_assumptions = {
    "vatOnRevenue" : 15,
    "vatOnCost" : 15,
    "vatOnConstructionCost" :15
    }
percentage_of_cost_application_for_vat ={
    "developmentAndProjectManagement" : 100,
    "turbineCost" : 100,
    "civilWork" : 100,
    "logisticsAndOthers" : 100,
    "developerFee" : 100
    }
vat_settlement_period = 60

cost_of_funds = {
    "costOfEquity" : 6.7632,
    "costOfDebtPreTax" : construction_debt_assumption["libor"] + construction_debt_assumption["margin"]
    }


# 2.07 Depreciation Assumptions

dep_years = {
    "devAndProManagementYears" : 40,
    "turbineCostYears" : 40,
    "civilWorkYears" : 40,
    "logisticsAndOthersYears" : 40,
    "developerFeeYears" : 40
    }
dep_method = "straightMethod"


def initial():
    file_path = "C:\\Users\\admin\\Desktop\\Wind\\Wind back from repo\\Wind_Backend\\backend\\app\\api\\routes\\project_parameters.json"
    with open(file_path, 'r') as val:
        global values
        values = json.load(val)
        
    modelTimingData = [1, 3, 6, 12]
    global modelling_time_interval
    modelling_time_interval = 1
    global construction_start_date
    construction_start_date = next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["construction_start_date"]

    global construction_period_in_months
    construction_period_in_months = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["construction_period_in_months"])

    global operation_period
    operation_period = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["operation_period"])

    global decommissioning_period
    decommissioning_period = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["decommissioning_period"])


    # Turibine assumptions

    global capacity_per_turbine
    capacity_per_turbine = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["capacity_per_turbine"])

    global number_of_turbines
    number_of_turbines = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["number_of_turbine"])

    global capacity_factor_data
    capacity_factor_data = [0.25,0.27,0.29,0.3,0.32]

    global capacity_factor_apply_period_data
    capacity_factor_apply_period_data = [12,18,18,20]

    # Indexation assumptions

   

    # Revenue assumptions

    global feed_in_tariff_price_per_mw
    feed_in_tariff_price_per_mw = {
        "unitCost":float(next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["fit_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["fit_inflation_profile"]-1]
        }

    global merchant_price_per_mwh
    merchant_price_per_mwh = {
        "unitCost":float(next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["merchant_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["merchant_inflation_profile"]-1]
        }

    global revenue_from_others_per_month
    revenue_from_others_per_month = {
        "unitCost":float(next((p for p in values if p['param_index'] == "revenue@revenue_from_others"), None)["value"]["base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "revenue@revenue_from_others"), None)["value"]["other_revenue_inflation_profile"]-1]
        }

    global ppaTerm
    ppaTermVal = int(next((p for p in values if p['param_index'] == "revenue@power_purachase_agreement"), None)["value"]["base_case"]),
    ppaTerm = ppaTermVal[0]

    global electricity_sold_percentage_during_ppa_term
    electricitySoldPercentage = next((p for p in values if p['param_index'] == "revenue@power_purachase_agreement"), None)["value"]["electricity_sold_percen_base_case"],
    electricity_sold_percentage_during_ppa_term = float(electricitySoldPercentage[0]) / 100

    # Variable O&M Cost Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.01

    global staff_cost_per_mwh
    global equipment_cost_per_mwh
    global consumables_cost_per_mwh
    global fuel_cost_per_mwh
    global transport_cost_per_mwh
    global maintenance_cost_per_mwh

    staff_cost_per_mwh = {
        "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["staff_cost_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["staff_cost_inflaion_profile"]-1]
        }
    equipment_cost_per_mwh = {
        "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["equipment_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["equipment_inflaion_profile"]-1]
        }
    consumables_cost_per_mwh = {
        "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["fuel_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["consumables_inflaion_profile"]-1]
        }
    fuel_cost_per_mwh = {
        "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["consumables_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["fuel_inflaion_profile"]-1]
        }
    transport_cost_per_mwh = {
        "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["transport_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["transport_inflaion_profile"]-1]
        }
    maintenance_cost_per_mwh = {
        "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["maintenance_base_case"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["maintenance_inflaion_profile"]-1]
        }

    # Other Fixed Costs Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.02
    # unit of fixed costs is 1000
    global spv_costs_per_year
    global insurance_per_year
    global land_lease_per_year
    global security_per_year
    global community_per_year
    global management_fee_per_year

    spv_costs_per_year = {
        "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["spv_annual_cost"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["spv_inflaion_profile"]-1]
        }
    insurance_per_year = {
        "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["insurance_annual_cost"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["land_inflaion_profile"]-1]
        }
    land_lease_per_year = {
        "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["land_annual_cost"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["insurance_inflaion_profile"]-1]
        }
    security_per_year = {
        "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["security_annual_cost"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["security_inflaion_profile"]-1]
        }
    community_per_year = {
        "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["community_annual_cost"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["community_inflaion_profile"]-1]
        }
    management_fee_per_year = {
        "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["management_annual_cost"]),
        "inflationProfile":inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["management_inflaion_profile"]-1]
        }

    # Construction cost assumption ~~~ Assumptions sheet/2 Construction Cost
    # Development and Project Management
    development_and_consenting_service_per_mw = 50
    environmental_surveys_per_mw = 5.15
    resource_and_met_ocean_assessment_per_mw = 5.15
    geological_and_hydrographical_surveys_per_mw = 5.15
    engineering_and_consultancy = 5.15

    # Turbine Cost
    wind_turbine_cost_per_mw = 500

    # Civil Work
    civil_work_Expenditure_per_mw = 350
    balance_of_plant_expenditure_per_mw = 300

    # Logistics and Others
    logistics_and_others_expenditure_per_mw = 0

    # Developer's Fee
    developer_fee_percentage = 1

    # Capex Phasing

    capex_phasing_data = {
        "developmentAndProjectManagement":[50,50,0,0],
        "turbineCost":[0,35,35,30],
        "civilWork":[0,35,35,30],
        "logisticsAndOthers":[0,35,35,30],
        "developerFee":[0,100,0,0]
    }

    global decommissioning_total_cost
    decommissioning_total_cost = 1000

    # 6 Financing Assumptions

    # 6.01 Debt Equity Ratio
    global debt_ratio
    global equity_ratio
    debtRate = next((p for p in values if p['param_index'] == "financing"), None)["value"]["debt_ratio"], 
    debt_ratio = float(debtRate[0])
    equity_ratio = 100 - debt_ratio

    # 6.03 Construction Debt Assumptions
    global construction_debt_assumption
    construction_debt_assumption = {
        "constructionDebtTenure" : int(next((p for p in values if p['param_index'] == "financing"), None)["value"]["construction_debt_tenure"]), 
        "repaymentStartDate" : datetime.datetime.strptime(construction_start_date,'%Y-%m-%d') + relativedelta(months=+construction_period_in_months),
        "libor":float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["libor"]),
        "margin":float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["margin"]),
        "dscr" : float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["target_dscr"])
        }

    # 6.07 Fees
    global fees_assumption
    fees_assumption = {
        "arrangementFeesPercentage" : float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["arrangement_fees"]),
        "commitmentFeesPercentage" : float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["commitment_fees"])
        }
    # 6.08 DSRA
    global dsra_years
    dsra_yearsVal = next((p for p in values if p['param_index'] == "financing"), None)["value"]["debt_service_period_to_be_considered_for_dsra_balance"],
    dsra_years = int(dsra_yearsVal[0])
    # 7 Other Assumptions
    global working_capital_days
    working_capital_days = {
        "receivableDays" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["receivable_days"]),
        "payableDays" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["payable_days"]),
        }
    global income_tax_assumptions
    income_tax_assumptions = {
        "incomeTaxRate" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["income_tax_rate"]),
        "taxHoliday" :0,
        "taxHolidayPeriod" :float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["tax_holiday_period"]),
        }
    global vat_assumptions
    vat_assumptions = {
        "vatOnRevenue" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_on_revenue"]),
        "vatOnCost" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_on_cost"]),
        "vatOnConstructionCost" :float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_on_construction_cost"])
        }
    global percentage_of_cost_application_for_vat
    percentage_of_cost_application_for_vat ={
        "developmentAndProjectManagement" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["development_and_project_management"]),
        "turbineCost" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["turbine_cost"]),
        "civilWork" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["civil_work"]),
        "logisticsAndOthers" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["logistics_and_others"]),
        "developerFee" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["developer_fee"]),
        }
    global vat_settlement_period
    vat_settlement_periodVal = next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_settlement_period"],
    vat_settlement_period = int(vat_settlement_periodVal[0])
    global cost_of_funds
    cost_of_funds = {
        "costOfEquity" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["cost_of_equity"]),
        "costOfDebtPreTax" : construction_debt_assumption["libor"] + construction_debt_assumption["margin"]
        }


    # 2.07 Depreciation Assumptions
    global dep_years
    dep_years = {
        "devAndProManagementYears" : 40,
        "turbineCostYears" : 40,
        "civilWorkYears" : 40,
        "logisticsAndOthersYears" : 40,
        "developerFeeYears" : 40
        }
    global dep_method

        
    #     dep_method = "straightMethod"
    # if __name__ == '__main__':
    #     initial()
