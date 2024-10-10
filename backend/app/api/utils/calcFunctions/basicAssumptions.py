import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import os
import json
import app.api.utils.calcFunctions.input as val

def get_cur_path():
    return os.path.dirname(os.path.realpath(__file__))

class BasicAssumptions:
    def __init__(self):
        self.modelling_time_interval = 6
        self.currency_unit = 1000
        # Timing assumptions
        self.modelling_time_interval = 6
        self.construction_start_date = "2021-01-01"
        self.construction_period_in_months = 24
        self.operation_period = 40
        self.decommissioning_period = 3
        # Turibine assumptions
        self.capacity_per_turbine = 3
        self.number_of_turbines = 20
        self.capacity_factor_data = [0.25,0.27,0.29,0.3,0.32]
        self.capacity_factor_apply_period_data = [12,18,18,20]
        # Indexation assumptions
        self.inflation_rate_data = [[0.020,0.020,0.025,0.025,0.0275,0.0275,0.030,0.030,0.030,0.030]]
        self.inflation_base_year = 2021
        # Revenue assumptions
        self.feed_in_tariff_price_per_mw = {"unitCost":110,"inflationProfile":self.inflation_rate_data[0]}
        self.merchant_price_per_mwh = {"unitCost":40,"inflationProfile":self.inflation_rate_data[0]}
        self.revenue_from_others_per_month = {"unitCost":25000,"inflationProfile":self.inflation_rate_data[0]}
        self.ppaTerm = 15
        self.electricity_sold_percentage_during_ppa_term = 0.8
        # Variable O&M Cost Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.01
        self.staff_cost_per_mwh = {"unitCost":10,"inflationProfile":self.inflation_rate_data[0]}
        self.equipment_cost_per_mwh = {"unitCost":3,"inflationProfile":self.inflation_rate_data[0]}
        self.consumables_cost_per_mwh = {"unitCost":1,"inflationProfile":self.inflation_rate_data[0]}
        self.fuel_cost_per_mwh = {"unitCost":1,"inflationProfile":self.inflation_rate_data[0]}
        self.transport_cost_per_mwh = {"unitCost":3,"inflationProfile":self.inflation_rate_data[0]}
        self.maintenance_cost_per_mwh = {"unitCost":3,"inflationProfile":self.inflation_rate_data[0]}
        # Other Fixed Costs Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.02
        # unit of fixed costs is 1000

        self.spv_costs_per_year = {"fixedCost":400,"inflationProfile":self.inflation_rate_data[0]}
        self.insurance_per_year = {"fixedCost":219.2,"inflationProfile":self.inflation_rate_data[0]}
        self.land_lease_per_year = {"fixedCost":8.5,"inflationProfile":self.inflation_rate_data[0]}
        self.security_per_year = {"fixedCost":200,"inflationProfile":self.inflation_rate_data[0]}
        self.community_per_year = {"fixedCost":45,"inflationProfile":self.inflation_rate_data[0]}
        self.management_fee_per_year = {"fixedCost":8.5,"inflationProfile":self.inflation_rate_data[0]}

        # Construction cost assumption ~~~ Assumptions sheet/2 Construction Cost
        # Development and Project Management
        self.development_and_consenting_service_per_mw = 50
        self.environmental_surveys_per_mw = 5.15
        self.resource_and_met_ocean_assessment_per_mw = 5.15
        self.geological_and_hydrographical_surveys_per_mw = 5.15
        self.engineering_and_consultancy = 5.15

        # Turbine Cost
        self.wind_turbine_cost_per_mw = 500

        # Civil Work
        self.civil_work_Expenditure_per_mw = 350
        self.balance_of_plant_expenditure_per_mw = 300

        # Logistics and Others
        self.logistics_and_others_expenditure_per_mw = 0

        # Developer's Fee
        self.developer_fee_percentage = 1

        # Capex Phasing

        self.capex_phasing_data = {
            "developmentAndProjectManagement":[50,50,0,0],
            "turbineCost":[0,35,35,30],
            "civilWork":[0,35,35,30],
            "logisticsAndOthers":[0,35,35,30],
            "developerFee":[0,100,0,0]
        }


        self.decommissioning_total_cost = 1000

        # 6 Financing Assumptions

        # 6.01 Debt Equity Ratio
        self.debt_ratio = 75
        self.equity_ratio = 100 - self.debt_ratio

        # 6.03 Construction Debt Assumptions

        self.construction_debt_assumption = {
            "constructionDebtTenure" : 20, 
            "repaymentStartDate" : datetime.datetime.strptime(self.construction_start_date,'%Y-%m-%d') + relativedelta(months=+self.construction_period_in_months),
            "libor":3,
            "margin":3,
            "dscr" : 1.5
            }

        # 6.07 Fees
        self.fees_assumption = {
            "arrangementFeesPercentage" : 0.3,
            "commitmentFeesPercentage" : 0.3
            }
        # 6.08 DSRA
        self.dsra_years = 1

        # 7 Other Assumptions

        self.working_capital_days = {
            "receivableDays" : 60,
            "payableDays" : 60
            }
        self.income_tax_assumptions = {
            "incomeTaxRate" : 20,
            "taxHoliday" : 0,
            "taxHolidayPeriod" :2
            }
        self.vat_assumptions = {
            "vatOnRevenue" : 15,
            "vatOnCost" : 15,
            "vatOnConstructionCost" :15
            }
        self.percentage_of_cost_application_for_vat ={
            "developmentAndProjectManagement" : 100,
            "turbineCost" : 100,
            "civilWork" : 100,
            "logisticsAndOthers" : 100,
            "developerFee" : 100
            }
        self.vat_settlement_period = 60

        self.cost_of_funds = {
            "costOfEquity" : 6.7632,
            "costOfDebtPreTax" : self.construction_debt_assumption["libor"] + self.construction_debt_assumption["margin"]
            }


        # 2.07 Depreciation Assumptions

        self.dep_years = {
            "devAndProManagementYears" : 40,
            "turbineCostYears" : 40,
            "civilWorkYears" : 40,
            "logisticsAndOthersYears" : 40,
            "developerFeeYears" : 40
            }
        self.dep_method = "straightMethod"
        self.values = []

        self.load_parameters()
    def load_parameters(self):
        """Load parameters from the JSON file."""
        current_dir = get_cur_path()
        file_name = 'project_parameters.json'
        file_path = os.path.join(current_dir, '..\\..', 'routes', file_name)
        try:
            with open(file_path, 'r') as f:
                values = json.load(f)
                self.modelling_time_interval = next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["modeling_time_interval"]
                self.construction_start_date = next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["construction_start_date"]
                self.construction_period_in_months = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["construction_period_in_months"])
                self.operation_period = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["operation_period"])
                self.decommissioning_period = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["decommissioning_period"])
                # Turibine assumptions
                self.capacity_per_turbine = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["capacity_per_turbine"])
                self.number_of_turbines = int(next((p for p in values if p['param_index'] == "basic_project_inputs"), None)["value"]["number_of_turbine"])
                self.capacity_factor_data = [0.25,0.27,0.29,0.3,0.32]
                self.capacity_factor_apply_period_data = [12,18,18,20]
                # Indexation assumptions
                # Revenue assumptions
                self.feed_in_tariff_price_per_mw = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["fit_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["fit_inflation_profile"]-1]
                    }
                self.merchant_price_per_mwh = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["merchant_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "revenue@tariff"), None)["value"]["merchant_inflation_profile"]-1]
                    }
                self.revenue_from_others_per_month = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "revenue@revenue_from_others"), None)["value"]["base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "revenue@revenue_from_others"), None)["value"]["other_revenue_inflation_profile"]-1]
                    }
                self.ppaTermVal = int(next((p for p in values if p['param_index'] == "revenue@power_purachase_agreement"), None)["value"]["base_case"]),
                self.ppaTerm = self.ppaTermVal[0]
                self.electricitySoldPercentage = next((p for p in values if p['param_index'] == "revenue@power_purachase_agreement"), None)["value"]["electricity_sold_percen_base_case"],
                self.electricity_sold_percentage_during_ppa_term = float(self.electricitySoldPercentage[0]) / 100
                # Variable O&M Cost Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.01
                self.staff_cost_per_mwh = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["staff_cost_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["staff_cost_inflaion_profile"]-1]
                    }
                self.equipment_cost_per_mwh = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["equipment_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["equipment_inflaion_profile"]-1]
                    }
                self.consumables_cost_per_mwh = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["fuel_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["consumables_inflaion_profile"]-1]
                    }
                self.fuel_cost_per_mwh = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["consumables_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["fuel_inflaion_profile"]-1]
                    }
                self.transport_cost_per_mwh = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["transport_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["transport_inflaion_profile"]-1]
                    }
                self.maintenance_cost_per_mwh = {
                    "unitCost":float(next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["maintenance_base_case"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@variable_o_and_m_cost"), None)["value"]["maintenance_inflaion_profile"]-1]
                    }

                # Other Fixed Costs Assumptions ~~~ Assumptions sheet/4 Operating Cost/4.02
                # unit of fixed costs is 1000
                self.spv_costs_per_year = {
                    "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["spv_annual_cost"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["spv_inflaion_profile"]-1]
                    }
                self.insurance_per_year = {
                    "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["insurance_annual_cost"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["land_inflaion_profile"]-1]
                    }
                self.land_lease_per_year = {
                    "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["land_annual_cost"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["insurance_inflaion_profile"]-1]
                    }
                self.security_per_year = {
                    "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["security_annual_cost"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["security_inflaion_profile"]-1]
                    }
                self.community_per_year = {
                    "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["community_annual_cost"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["community_inflaion_profile"]-1]
                    }
                self.management_fee_per_year = {
                    "fixedCost":float(next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["management_annual_cost"]),
                    "inflationProfile":self.inflation_rate_data[next((p for p in values if p['param_index'] == "operating_cost@other_fixed_costs"), None)["value"]["management_inflaion_profile"]-1]
                    }

                # Construction cost assumption ~~~ Assumptions sheet/2 Construction Cost
                # Development and Project Management
                self.development_and_consenting_service_per_mw = 50
                self.environmental_surveys_per_mw = 5.15
                self.resource_and_met_ocean_assessment_per_mw = 5.15
                self.geological_and_hydrographical_surveys_per_mw = 5.15
                self.engineering_and_consultancy = 5.15

                # Turbine Cost
                self.wind_turbine_cost_per_mw = 500

                # Civil Work
                self.civil_work_Expenditure_per_mw = 350
                self.balance_of_plant_expenditure_per_mw = 300

                # Logistics and Others
                self.logistics_and_others_expenditure_per_mw = 0

                # Developer's Fee
                self.developer_fee_percentage = 1

                # Capex Phasing

                self.capex_phasing_data = {
                    "developmentAndProjectManagement":[50,50,0,0],
                    "turbineCost":[0,35,35,30],
                    "civilWork":[0,35,35,30],
                    "logisticsAndOthers":[0,35,35,30],
                    "developerFee":[0,100,0,0]
                }
                self.decommissioning_total_cost = 1000
                # 6 Financing Assumptions

                # 6.01 Debt Equity Ratio
                self.debtRate = next((p for p in values if p['param_index'] == "financing"), None)["value"]["debt_ratio"], 
                self.debt_ratio = float(self.debtRate[0])
                self.equity_ratio = 100 - self.debt_ratio

                # 6.03 Construction Debt Assumptions
                self.construction_debt_assumption = {
                    "constructionDebtTenure" : int(next((p for p in values if p['param_index'] == "financing"), None)["value"]["construction_debt_tenure"]), 
                    "repaymentStartDate" : datetime.datetime.strptime(self.construction_start_date,'%Y-%m-%d') + relativedelta(months=+self.construction_period_in_months),
                    "libor":float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["libor"]),
                    "margin":float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["margin"]),
                    "dscr" : float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["target_dscr"])
                    }

                # 6.07 Fees
                self.fees_assumption = {
                    "arrangementFeesPercentage" : float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["arrangement_fees"]),
                    "commitmentFeesPercentage" : float(next((p for p in values if p['param_index'] == "financing"), None)["value"]["commitment_fees"])
                    }
                # 6.08 DSRA
                self.dsra_yearsVal = next((p for p in values if p['param_index'] == "financing"), None)["value"]["debt_service_period_to_be_considered_for_dsra_balance"],
                self.dsra_years = int(self.dsra_yearsVal[0])
                # 7 Other Assumptions
                self.working_capital_days = {
                    "receivableDays" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["receivable_days"]),
                    "payableDays" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["payable_days"]),
                    }
                self.income_tax_assumptions = {
                    "incomeTaxRate" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["income_tax_rate"]),
                    "taxHoliday" :0,
                    "taxHolidayPeriod" :float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["tax_holiday_period"]),
                    }
                self.vat_assumptions = {
                    "vatOnRevenue" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_on_revenue"]),
                    "vatOnCost" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_on_cost"]),
                    "vatOnConstructionCost" :float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_on_construction_cost"])
                    }
                self.percentage_of_cost_application_for_vat ={
                    "developmentAndProjectManagement" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["development_and_project_management"]),
                    "turbineCost" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["turbine_cost"]),
                    "civilWork" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["civil_work"]),
                    "logisticsAndOthers" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["logistics_and_others"]),
                    "developerFee" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["developer_fee"]),
                    }
                self.vat_settlement_periodVal = next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["vat_settlement_period"],
                self.vat_settlement_period = int(self.vat_settlement_periodVal[0])
                self.cost_of_funds = {
                    "costOfEquity" : float(next((p for p in values if p['param_index'] == "other_assumptions"), None)["value"]["cost_of_equity"]),
                    "costOfDebtPreTax" : self.construction_debt_assumption["libor"] + self.construction_debt_assumption["margin"]
                    }

                # 2.07 Depreciation Assumptions
                self.dep_years = {
                    "devAndProManagementYears" : 40,
                    "turbineCostYears" : 40,
                    "civilWorkYears" : 40,
                    "logisticsAndOthersYears" : 40,
                    "developerFeeYears" : 40
                    }

        except FileNotFoundError:
            print("Parameter file not found. Using default values.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Using default values.")
    def initial(self):
        self.load_parameters()
        
basInputs = BasicAssumptions()


# def initial():
    # print("First Initial")
    # current_dir = get_cur_path()
    # file_name = 'project_parameters.json'
    # file_path = os.path.join(current_dir, '..\\..', 'routes', file_name)
    # with open(file_path, 'r') as val:
    #     global values
    #     values = json.load(val)
        
    # modelTimingData = [1, 3, 6, 12]
   
    #     dep_method = "straightMethod"
    # if __name__ == '__main__':
    #     initial()
