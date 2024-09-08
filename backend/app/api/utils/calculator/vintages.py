from app.api.utils.calculator.basic_functions import *
from app.api.utils.calculator.vintages import *
def calcVintages(revenueSetup, assumptionsData, detailedRevenueData, initialCycleData, initialCapacity, startingAssumptionsForBatteries, batteryDisposals, batteryEfficiency, batteryAugmentation, model, batteryDuration, batteryCubes, batteryExCubes, inflationInputs, capexPaymentsProfile, capexPaymentMilestones, capexUEL, bessCapexForecast, sensitivity, operationYears, modelStartDate, operationStartDate, decommissioningEndDate, decommissioningStartDate):
    period = getMonthsNumberFromModelStartDate(modelStartDate, decommissioningEndDate) - 1
    diposalMonth = getMonthsNumberFromModelStartDate(modelStartDate, decommissioningStartDate)
    vintages = []
    for i in range(40):
        vintages.append({
            'name': f'Vintage{i + 1}',
            'data': {
                'stagingMonthNumber': None,
                'stagingFlag': "",
                'additionsCost': "",
                'paymentMilestones': "",
                'forecastAdditionsByMilestones': [],
                'grossCashPayments': "",
                'forecastDepreciationChargeByPeriod': [],
                'startBalance': [0],
                'endBalance': [],
                'disposalMonthNumber': "",
                'disposalFlag': 0,
                'capacityPreAdjustmentForEfficiency': "",
                'capacityAddedAdjustedForEfficiency': "",
                'capacityPostEfficiencyAndDegradation': "",
                'cumulativeDegradation': "",
                'degradationInPeriod': "",
                'generationCapacityInPeriod': "",
                'forecastCapexPrice': "",
                'forecastCapexAdditions': "",
            },
        }) 
    degradationPerCycle = get_live_degradation_per_cycle(initialCycleData, startingAssumptionsForBatteries)
    cyclesPerPeriod = get_cycles_per_month(revenueSetup, assumptionsData, startingAssumptionsForBatteries, detailedRevenueData, modelStartDate, operationStartDate, operationYears)
    print(len(cyclesPerPeriod))

    capexForecast = annual_index_to_months(calc_capex_forecast(model, batteryDuration, batteryCubes, batteryExCubes, inflationInputs, bessCapexForecast, sensitivity, operationYears)[2])

    bessPaymentProfile = next(item for item in capexPaymentMilestones if item["profileName"] == next(d for d in capexPaymentsProfile if d["capexObject"] == "Batteries")["paymentProfile"])["timing"]
    paymentProfileLength = len(bessPaymentProfile)
    batteriesUEL = next(d for d in capexUEL if d["capexObject"] == "Batteries")["usefulEconomicLife"]
    vintages[0]['data']['stagingMonthNumber'] = getMonthsNumberFromModelStartDate(modelStartDate, operationStartDate)
    vintages[0]['data']['capacityPreAdjustmentForEfficiency'] = initialCapacity
    vintages[0]['data']['capacityAddedAdjustedForEfficiency'] = round((vintages[0]['data']['capacityPreAdjustmentForEfficiency'] * 100) / batteryEfficiency['fixedEfficiency'], 4)
    vintages[0]['data']['additionsCost'] = capexForecast[vintages[0]['data']['stagingMonthNumber'] - 1] * vintages[0]['data']['capacityAddedAdjustedForEfficiency']

    totalGenerationCapacity = [0]*period
    decommissioningStratMonthNumber = getMonthsNumberFromModelStartDate(modelStartDate, decommissioningStartDate)
 
    totalGenerationCapacity = [0]*period

    for k in range(40):
        degradationValue = [0]*period
        generationCapacity = [0]*period
        cumulativeDegradationValue = 0
        paymentSchedule = [0]*period

        for i in range(period): 
            if i >= vintages[k]['data']['stagingMonthNumber'] - paymentProfileLength and i < vintages[k]['data']['stagingMonthNumber']:
                paymentSchedule[i] = bessPaymentProfile[i + paymentProfileLength - vintages[k]['data']['stagingMonthNumber']]
            else:
                paymentSchedule[i] = 0

            vintages[k]['data']['forecastAdditionsByMilestones'].append(round(paymentSchedule[i] * vintages[k]['data']['additionsCost'], 2))

            if vintages[k]['data']['stagingMonthNumber'] - 1 > i or vintages[k]['data']['disposalFlag'] == 1 or i >= diposalMonth:
                degradationValue[i] = 0
                generationCapacity[i] = 0
                cumulativeDegradationValue += degradationValue[i]
            else:
                if i >= diposalMonth - 1:
                    degradationValue[i] = 0
                else:
                    degradationValue[i] = degradationPerCycle[i - vintages[k]['data']['stagingMonthNumber'] + 1] * cyclesPerPeriod[i]

                cumulativeDegradationValue += degradationValue[i]
                generationCapacity[i] = round(vintages[k]['data']['capacityPreAdjustmentForEfficiency'] * (1 - cumulativeDegradationValue), 4)

            monthlyDepreciationAmount = vintages[k]['data']['additionsCost'] / (12 * batteriesUEL)

        for j in range(period):
            if j >= vintages[k]['data']['stagingMonthNumber'] - 1 and j < vintages[k]['data']['disposalMonthNumber'] - 1 and j < vintages[k]['data']['stagingMonthNumber'] + 12 * batteriesUEL - 1:
                vintages[k]['data']['forecastDepreciationChargeByPeriod'].append(monthlyDepreciationAmount)
            else:
                vintages[k]['data']['forecastDepreciationChargeByPeriod'].append(0)

            vintages[k]['data']['endBalance'].append(vintages[k]['data']['startBalance'][j] + vintages[k]['data']['forecastAdditionsByMilestones'][j] - vintages[k]['data']['forecastDepreciationChargeByPeriod'][j])

            if j < period - 1:
                vintages[k]['data']['startBalance'].append(vintages[k]['data']['endBalance'][j])

        vintages[k]['data']['cumulativeDegradation'] = cumulativeDegradationValue
        vintages[k]['data']['generationCapacityInPeriod'] = generationCapacity
        totalGenerationCapacity = [sum(x) for x in zip(totalGenerationCapacity, vintages[k]['data']['generationCapacityInPeriod'])]

        vintages[k]['data']['paymentMilestones'] = paymentSchedule

        if k < 39:
            vintages[k + 1]['data']['stagingMonthNumber'] = vintages[k]['data']['stagingMonthNumber'] + 12
            vintages[k + 1]['data']['capacityPreAdjustmentForEfficiency'] = round(initialCapacity - totalGenerationCapacity[vintages[k + 1]['data']['stagingMonthNumber'] - 1], 2)
            vintages[k + 1]['data']['capacityAddedAdjustedForEfficiency'] = round((vintages[k + 1]['data']['capacityPreAdjustmentForEfficiency'] * 100) / batteryEfficiency['fixedEfficiency'], 4)
            vintages[k + 1]['data']['additionsCost'] = capexForecast[vintages[k + 1]['data']['stagingMonthNumber'] - 1] * vintages[k + 1]['data']['capacityAddedAdjustedForEfficiency']

    return {
        'vintages': vintages,
        'totalGenerationCapacity': totalGenerationCapacity,
    }
