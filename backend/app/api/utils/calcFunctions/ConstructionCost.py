import app.api.utils.calcFunctions.basicAssumptions as basInputs
import app.api.utils.calcFunctions.basicResults as basResult
from app.api.utils.calcFunctions.basicFun import arrayFillWithZeros
from app.api.utils.calcFunctions.basicFun import multiplyArrayByNumber
from app.api.utils.calcFunctions.basicFun import multiplyArrays
from app.api.utils.calcFunctions.basicFun import sumArrays
from app.api.utils.calcFunctions.basicFun import calcSumOfValuesOfTheArray


inp = basInputs.basInputs
# Non circular part
global interest_rate
interest_rate = pow((1 + inp.construction_debt_assumption["libor"] / 100 + inp.construction_debt_assumption["margin"] / 100),inp.modelling_time_interval / 12) - 1

global development_and_project_management_per_period
global turbine_cost_per_period
global civil_work_per_period
global logistics_and_others_per_period
global developer_fee_per_period
global total_construction_cost_before_idc_and_fees

development_and_project_management_per_period = multiplyArrayByNumber(arrayFillWithZeros(inp.capex_phasing_data["developmentAndProjectManagement"], basResult.calculation_period), basResult.totalDevelopmentAndProject / 100)
turbine_cost_per_period = multiplyArrayByNumber(arrayFillWithZeros(inp.capex_phasing_data["turbineCost"], basResult.calculation_period), basResult.total_turbine_cost / 100)
civil_work_per_period = multiplyArrayByNumber(arrayFillWithZeros(inp.capex_phasing_data["civilWork"], basResult.calculation_period), basResult.total_civil_work_expenditure / 100)
logistics_and_others_per_period = multiplyArrayByNumber(arrayFillWithZeros(inp.capex_phasing_data["logisticsAndOthers"], basResult.calculation_period), basResult.total_logistics_and_others_expenditure / 100)
developer_fee_per_period = multiplyArrayByNumber(arrayFillWithZeros(inp.capex_phasing_data["developerFee"], basResult.calculation_period), basResult.total_developer_fee / 100)
total_construction_cost_before_idc_and_fees = sumArrays(development_and_project_management_per_period,developer_fee_per_period,turbine_cost_per_period,civil_work_per_period,logistics_and_others_per_period)

# Construction sheet ~~~ Construction Period VAT
# 1.31 VAT on Construction Cost
global vat_on_development_and_project_management_per_period
global vat_on_turbine_cost_per_period
global vat_on_civil_work_per_period
global vat_on_logistics_and_others_per_period
global vat_on_developer_fee_per_period
global total_vat_on_construction_cost

vat_on_development_and_project_management_per_period = multiplyArrayByNumber(development_and_project_management_per_period, inp.vat_assumptions["vatOnConstructionCost"] / 100 * inp.percentage_of_cost_application_for_vat["developmentAndProjectManagement"] / 100  )
vat_on_turbine_cost_per_period = multiplyArrayByNumber(turbine_cost_per_period,inp.vat_assumptions["vatOnConstructionCost"] / 100 * inp.percentage_of_cost_application_for_vat["turbineCost"] / 100)
vat_on_civil_work_per_period =  multiplyArrayByNumber(civil_work_per_period, inp.vat_assumptions["vatOnConstructionCost"] / 100 * inp.percentage_of_cost_application_for_vat["civilWork"] / 100)
vat_on_logistics_and_others_per_period = multiplyArrayByNumber(logistics_and_others_per_period, inp.vat_assumptions["vatOnConstructionCost"] / 100 * inp.percentage_of_cost_application_for_vat["logisticsAndOthers"] / 100)
vat_on_developer_fee_per_period = multiplyArrayByNumber(developer_fee_per_period, inp.vat_assumptions["vatOnConstructionCost"] / 100 * inp.percentage_of_cost_application_for_vat["developerFee"] / 100)
total_vat_on_construction_cost = sumArrays(vat_on_developer_fee_per_period,vat_on_turbine_cost_per_period, vat_on_civil_work_per_period,vat_on_logistics_and_others_per_period,vat_on_development_and_project_management_per_period)


# 1.33 VAT on Development and construction Cost
global vat_on_dev_and_cons_cost_start_balance
global vat_paid_construction_cost_per_period
global vat_refund_monthly_period
global vat_refund_non_monthly_period
global vat_on_dev_and_cons_cost_closing_balance

vat_on_dev_and_cons_cost_start_balance = [0] * basResult.calculation_period
vat_on_dev_and_cons_cost_closing_balance = [0] * basResult.calculation_period
vat_paid_construction_cost_per_period = sumArrays(vat_on_development_and_project_management_per_period,vat_on_turbine_cost_per_period,vat_on_civil_work_per_period,vat_on_logistics_and_others_per_period)
vat_refund_monthly_period = [0] * basResult.calculation_period
vat_refund_non_monthly_period = [0] * basResult.calculation_period

# 1.34 VAT on Developer's Fee
global vat_on_dev_fee_start_balance
global vat_paid_dev_fee_per_period
global vat_refund_monthly_periodOnDevFee
global vat_refund_non_monthly_periodOnDevFee
global vat_on_dev_fee_closing_balance

vat_on_dev_fee_start_balance = [0] * basResult.calculation_period
vat_on_dev_fee_closing_balance = [0] * basResult.calculation_period
vat_paid_dev_fee_per_period = vat_on_developer_fee_per_period
vat_refund_monthly_periodOnDevFee = [0] * basResult.calculation_period
vat_refund_non_monthly_periodOnDevFee = [0] * basResult.calculation_period

# 1.32 VAT summary
global vat_summary_start_balance
global vat_summary_closing_balance

vat_summary_start_balance = [0] * basResult.calculation_period
vat_summary_closing_balance = [0] * basResult.calculation_period

# Calculation of 1.32, 1.33 and 1.34
def calcVATonDevAndConsCostAndDeveloperFee():
    index = 0
    if inp.modelling_time_interval == 1:
        while index < basResult.calculation_period:
            if index < inp.vat_settlement_period / 30:
                vat_refund_monthly_period[index] = 0
                vat_refund_non_monthly_period[index] = 0
                vat_refund_monthly_periodOnDevFee[index] = 0
                vat_refund_non_monthly_periodOnDevFee[index] = 0
            else:
                vat_refund_monthly_period[index] = vat_paid_construction_cost_per_period[index - int(inp.vat_settlement_period / 30)] * basResult.construction_period_flag[index]
                vat_refund_non_monthly_period[index] = 0
                vat_refund_monthly_periodOnDevFee[index] = vat_paid_dev_fee_per_period[index - int(inp.vat_settlement_period / 30)] * basResult.construction_period_flag[index]
                vat_refund_non_monthly_periodOnDevFee[index] = 0
            vat_on_dev_and_cons_cost_closing_balance[index] = vat_on_dev_and_cons_cost_start_balance[index] + vat_paid_construction_cost_per_period[index] + vat_refund_monthly_period[index] + vat_refund_non_monthly_period[index]
            vat_on_dev_fee_closing_balance[index] = vat_on_dev_fee_start_balance[index] + vat_paid_dev_fee_per_period[index] + vat_refund_monthly_periodOnDevFee[index] + vat_refund_non_monthly_periodOnDevFee[index]
            vat_summary_closing_balance[index] = (vat_summary_start_balance[index] + vat_paid_construction_cost_per_period[index] + vat_refund_monthly_period[index] + vat_refund_non_monthly_period[index] + vat_paid_dev_fee_per_period[index] + vat_refund_monthly_periodOnDevFee[index] + vat_refund_non_monthly_periodOnDevFee[index]) * basResult.construction_period_flag[index]
            if index < basResult.calculation_period - 1:
                vat_on_dev_and_cons_cost_start_balance[index + 1] = vat_on_dev_and_cons_cost_closing_balance[index]
                vat_on_dev_fee_start_balance[index + 1] = vat_on_dev_fee_closing_balance[index]
                vat_summary_start_balance[index + 1] = vat_summary_closing_balance[index] 
            index += 1
    else:
        while index < basResult.calculation_period:
            vat_refund_monthly_period[index] = 0
            vat_refund_non_monthly_period[index] = (vat_paid_construction_cost_per_period[index] * inp.vat_settlement_period / basResult.daysInPeriod[index] - (vat_on_dev_and_cons_cost_start_balance[index] + vat_paid_construction_cost_per_period[index])) * basResult.construction_period_flag[index]
            vat_on_dev_and_cons_cost_closing_balance[index] = vat_on_dev_and_cons_cost_start_balance[index] + vat_paid_construction_cost_per_period[index] + vat_refund_monthly_period[index] + vat_refund_non_monthly_period[index]
            vat_refund_monthly_periodOnDevFee[index] = 0
            vat_refund_non_monthly_periodOnDevFee[index] = (vat_paid_dev_fee_per_period[index] * inp.vat_settlement_period / basResult.daysInPeriod[index] - (vat_on_dev_fee_start_balance[index] + vat_paid_dev_fee_per_period[index])) * basResult.construction_period_flag[index]
            vat_on_dev_fee_closing_balance[index] = vat_on_dev_fee_start_balance[index] + vat_paid_dev_fee_per_period[index] + vat_refund_monthly_periodOnDevFee[index] + vat_refund_non_monthly_periodOnDevFee[index]
            vat_summary_closing_balance[index] = (vat_summary_start_balance[index] + vat_paid_construction_cost_per_period[index] + vat_refund_monthly_period[index] + vat_refund_non_monthly_period[index] + vat_paid_dev_fee_per_period[index] + vat_refund_monthly_periodOnDevFee[index] + vat_refund_non_monthly_periodOnDevFee[index]) * basResult.construction_period_flag[index]
            
            if index < basResult.calculation_period - 1:
                vat_on_dev_and_cons_cost_start_balance[index + 1] = vat_on_dev_and_cons_cost_closing_balance[index] * basResult.construction_period_flag[index + 1]
                vat_on_dev_fee_start_balance[index + 1] = vat_on_dev_fee_closing_balance[index] * basResult.construction_period_flag[index + 1]
                vat_summary_start_balance[index + 1] = vat_summary_closing_balance[index] 
            index += 1

    vat_summary_movement = sumArrays(vat_paid_construction_cost_per_period, vat_paid_dev_fee_per_period, vat_refund_monthly_period,vat_refund_monthly_periodOnDevFee,vat_refund_non_monthly_period, vat_refund_non_monthly_periodOnDevFee)
    return {
        "vat_summary_start_balance" : vat_summary_start_balance,
        "vat_summary_closing_balance" : vat_summary_closing_balance,
        "vat_summary_movement" : vat_summary_movement
        }


global total_debt_per_period
global total_equity_per_period
total_debt_per_period = multiplyArrayByNumber(total_construction_cost_before_idc_and_fees, inp.debt_ratio / 100)
total_equity_per_period = multiplyArrayByNumber(total_construction_cost_before_idc_and_fees, inp.equity_ratio / 100)


global interest_during_construction_per_period
global cumulative_debt_per_period
global arrangement_fee_per_period
global commitment_fee_per_period
global dsra_initial_funding_per_period
global debt_to_be_serviced_per_period
global funding_delta_per_period
global total_construction_cost_per_period


interest_during_construction_per_period = [0] * basResult.calculation_period
cumulative_debt_per_period = [0] * basResult.calculation_period
arrangement_fee_per_period = [0] * basResult.calculation_period
commitment_fee_per_period = [0] * basResult.calculation_period
debt_to_be_serviced_per_period = [0] * basResult.calculation_period
debtInitialFundingPerPeriod = [0] * basResult.calculation_period
funding_delta_per_period = multiplyArrayByNumber(basResult.construction_period_flag, 1000)

global money_raised_per_period
money_raised_per_period = total_construction_cost_before_idc_and_fees

total_money_raised = calcSumOfValuesOfTheArray(money_raised_per_period)

global money_avaialable_for_only_construction_per_period
money_avaialable_for_only_construction_per_period = [0.1] * basResult.calculation_period


iteration_counter = 0
def doIteration():
    calcVATonDevAndConsCostAndDeveloperFee()
    global money_avaialable_for_only_construction_per_period
    global money_raised_per_period
    
    while basResult.totalCapexSummaryAndPhasing - calcSumOfValuesOfTheArray(money_avaialable_for_only_construction_per_period) > 0.01:
        calcFunding()
        # money_raised_per_period = sumArrays(money_raised_per_period,interest_during_construction_per_period,arrangement_fee_per_period,commitment_fee_per_period,dsra_initial_funding_per_period)
        money_raised_per_period = sumArrays(money_raised_per_period,total_construction_cost_before_idc_and_fees,multiplyArrayByNumber(money_avaialable_for_only_construction_per_period,-1))
        
    return money_avaialable_for_only_construction_per_period

def calcFunding():

    global iteration_counter
    iteration_counter += 1

    global total_money_raised
    total_money_raised = calcSumOfValuesOfTheArray(money_raised_per_period)

    global total_debt_per_period
    total_debt_per_period = multiplyArrayByNumber(money_raised_per_period, inp.debt_ratio / 100)
    
    global total_debt_amount
    total_debt_amount = total_money_raised * inp.debt_ratio / 100

    global monthly_debt_repayment_amount
    monthly_debt_repayment_amount = total_debt_amount * pow(1 + interest_rate, inp.construction_debt_assumption["constructionDebtTenure"]  * 12 / inp.modelling_time_interval) * interest_rate / (pow(1 + interest_rate, inp.construction_debt_assumption["constructionDebtTenure"] * 12 / inp.modelling_time_interval) - 1)

    index = 0
    while index < basResult.calculation_period:
        if index == 0:            
            cumulative_debt_per_period[index] = total_debt_per_period[index]
            if total_debt_per_period[index] > 0:
                arrangement_fee_per_period[index] = total_debt_amount * inp.fees_assumption["arrangementFeesPercentage"] / 100
            else:
                arrangement_fee_per_period[index] = 0
            debt_to_be_serviced_per_period[index] = basResult.constructionDebtTenureFlag[index] * monthly_debt_repayment_amount
        else:
            cumulative_debt_per_period[index] = cumulative_debt_per_period[index - 1] + total_debt_per_period[index]    
            if (total_debt_per_period[index] > 0) and (total_debt_per_period[index - 1] == 0) :
                arrangement_fee_per_period[index] = total_debt_amount * inp.fees_assumption["arrangementFeesPercentage"] / 100
            else:
                arrangement_fee_per_period[index] = 0
            debt_to_be_serviced_per_period[index] = basResult.constructionDebtTenureFlag[index] * monthly_debt_repayment_amount

        commitment_fee_per_period[index] = max(total_debt_amount - cumulative_debt_per_period[index], 0) * inp.fees_assumption["commitmentFeesPercentage"] / (100 * 12)
        interest_during_construction_per_period[index] = cumulative_debt_per_period[index] * interest_rate * basResult.construction_period_flag[index]

        index += 1

    j = 0

    global dsra_initial_funding_per_period
    dsra_initial_funding_per_period = [0] * basResult.calculation_period
    
    while j < basResult.calculation_period:
        if basResult.dsraInitialFundingDateFlag[j] == 0:
            dsra_initial_funding_per_period[j] = 0
            
        else:
            k = 1
            while k <= basResult.dsra_forward_periods: 
                dsra_initial_funding_per_period[j] += debt_to_be_serviced_per_period[j+k]
                k += 1
                
        money_avaialable_for_only_construction_per_period[j] = money_raised_per_period[j] - (interest_during_construction_per_period[j] + arrangement_fee_per_period[j] + commitment_fee_per_period[j] + dsra_initial_funding_per_period[j] + vat_on_developer_fee_per_period[j] + vat_paid_construction_cost_per_period[j] + vat_refund_monthly_period[j] + vat_refund_non_monthly_period[j] + vat_refund_monthly_periodOnDevFee[j] + vat_refund_non_monthly_periodOnDevFee[j])
        # money_raised_per_period[j] =total_construction_cost_before_idc_and_fees[j] + (interest_during_construction_per_period[j] + arrangement_fee_per_period[j] + commitment_fee_per_period[j] + dsra_initial_funding_per_period[j])
        j += 1

    return iteration_counter

# Construction sheet ~~~ 1.23 Construction Cost Summary
doIteration()

global dev_and_pro_management_per_period_for_dep
global turbine_cost_per_period_for_dep
global civil_work_per_period_for_dep
global logistics_and_others_per_period_for_dep
global developer_fee_per_period_for_dep

dev_and_pro_management_per_period_for_dep = [0] * basResult.calculation_period
turbine_cost_per_period_for_dep = [0] * basResult.calculation_period
civil_work_per_period_for_dep = [0] * basResult.calculation_period
logistics_and_others_per_period_for_dep = [0] * basResult.calculation_period
developer_fee_per_period_for_dep = [0] * basResult.calculation_period

global other_cons_cost
other_cons_cost = sumArrays(interest_during_construction_per_period, arrangement_fee_per_period, commitment_fee_per_period)
def calcConsCostSummary():
    index = 0
    while index < basResult.calculation_period:
        if total_construction_cost_before_idc_and_fees[index] == 0:
            dev_and_pro_management_per_period_for_dep[index] = development_and_project_management_per_period[index] + other_cons_cost[index] * basResult.totalDevelopmentAndProject / basResult.totalCapexSummaryAndPhasing
            turbine_cost_per_period_for_dep[index] = turbine_cost_per_period[index] + other_cons_cost[index] * basResult.total_turbine_cost/ basResult.totalCapexSummaryAndPhasing
            civil_work_per_period_for_dep[index] = civil_work_per_period[index] + other_cons_cost[index] * basResult.total_civil_work_expenditure/ basResult.totalCapexSummaryAndPhasing
            logistics_and_others_per_period_for_dep[index] = logistics_and_others_per_period[index] + other_cons_cost[index] * basResult.total_logistics_and_others_expenditure / basResult.totalCapexSummaryAndPhasing
            developer_fee_per_period_for_dep[index] = developer_fee_per_period[index] + other_cons_cost[index] * basResult.total_developer_fee/ basResult.totalCapexSummaryAndPhasing

        else:
            dev_and_pro_management_per_period_for_dep[index] = development_and_project_management_per_period[index] + development_and_project_management_per_period[index] * other_cons_cost[index] / total_construction_cost_before_idc_and_fees[index]
            turbine_cost_per_period_for_dep[index] = turbine_cost_per_period[index] + other_cons_cost[index] * turbine_cost_per_period[index] / total_construction_cost_before_idc_and_fees[index]
            civil_work_per_period_for_dep[index] = civil_work_per_period[index] + other_cons_cost[index] * civil_work_per_period[index] / total_construction_cost_before_idc_and_fees[index]
            logistics_and_others_per_period_for_dep[index] = logistics_and_others_per_period[index] + other_cons_cost[index] * logistics_and_others_per_period[index] / total_construction_cost_before_idc_and_fees[index]
            developer_fee_per_period_for_dep[index] = developer_fee_per_period[index] + other_cons_cost[index] * developer_fee_per_period[index] / total_construction_cost_before_idc_and_fees[index]
        index += 1

    return {
        "dev_and_pro_management_per_period_for_dep" : dev_and_pro_management_per_period_for_dep,
        "turbine_cost_per_period_for_dep" : turbine_cost_per_period_for_dep,
        "civil_work_per_period_for_dep" : civil_work_per_period_for_dep,
        "logistics_and_others_per_period_for_dep" : logistics_and_others_per_period_for_dep,
        "developer_fee_per_period_for_dep" : developer_fee_per_period_for_dep
        }
# Funding sheet ~~~ 1.34 Debt Summary Account
def calcDebtSummaryAccount():
    startBalance = [0] * basResult.calculation_period
    debtDrawdownsPerPeriod = total_debt_per_period
    closingBalace = [0] * basResult.calculation_period
    interest_accrued_per_period = [0] * basResult.calculation_period
    interest_paid_per_period = [0] * basResult.calculation_period
    repayments_per_period = [0] * basResult.calculation_period
    index = 0
    while index < basResult.calculation_period:
        interest_accrued_per_period[index] = (startBalance[index] + debtDrawdownsPerPeriod[index]) * interest_rate * basResult.constructionDebtTenureFlag[index]
        interest_paid_per_period[index] = - interest_accrued_per_period[index]
        repayments_per_period[index] = -( monthly_debt_repayment_amount + interest_paid_per_period[index] ) * basResult.constructionDebtTenureFlag[index]
        closingBalace[index] = startBalance[index] + debtDrawdownsPerPeriod[index] + interest_accrued_per_period[index] + interest_paid_per_period[index] + repayments_per_period[index]

        if index < basResult.calculation_period - 1:
            startBalance[index + 1] = closingBalace[index]
        index += 1
        

    return {
            "interest_accrued_per_period" : interest_accrued_per_period,
            "interest_paid_per_period" : interest_paid_per_period,
            "startBalance" : startBalance,
            "closingBalace" : closingBalace,
            "repayments_per_period" : repayments_per_period
            }
