def inflation_index(inflation_inputs, base_year=2023, profile="CPI to 2050 then nil"):
    match_data = next(item for item in get_inflation_index(inflation_inputs) if item["profile"] == profile)["rate"]
    inflation_result = []

    base_value = match_data[base_year - 2021]
    inflation_result = [m / base_value for m in match_data]
    return inflation_result

def getInflationIndex(inflationInputs):
    inflationIndex = []
    for d in inflationInputs:
        inflationIndex.append({
            'profile': d['profile'],
            'rate': round_array(cumulative_multiply(d['rate']), 10)
        })
    return inflationIndex

def get_cycles_per_month(
    revenue_setup = {
        "forecastProviderChoice": "Modo",
        "inflation": "CPI to 2050 then nil",
        "baseYear": 2023,
    },
    assumptions_data = [
        {
            "providerName": "Modo",
            "data": {
                "efficiency": 88,
                "inflation": "FES to 2050 then nil",
                "baseYear": 2023,
                "region": "Northern",
                "tradingStrategy": "Merchant and ancillaries",
            },
        },
    ],
    starting_assumptions_for_batteries = {
        "degradationForecastAverageCyclesPerDay": 1.25,
        "batteryAvailability": 97,
        "batteryDuration": 4,
    },
    detailed_revenue_data = None,
    model_start_date = "2023-01-01",
    operation_start_date = "2028-01-01",
    decommissioningEndDate = "2068-06-30"
    operation_years = 40
):
    number_of_days_in_month = calc_number_of_days_in_month(
        model_start_date,
        decommissioningEndDate
    )
    cycles_per_day = next((d for d in getActiveScenarioRevenueItems(
        revenue_setup,
        assumptions_data,
        starting_assumptions_for_batteries,
        detailed_revenue_data
    ) if d.get('item') == "Avg. Cycles per day"), {}).get('data')

    operations_as_a_percent_of_period = get_operations_as_a_percent_of_period(
        model_start_date,
        operation_start_date,
        operation_years
    )
    average_cycles_per_month = [
        round(
            d * cycles_per_day[i] * operations_as_a_percent_of_period[i], 3
        ) for i, d in enumerate(number_of_days_in_month)
    ]
    return average_cycles_per_month

def calc_capex_forecast(
    model = "Conservative",
    battery_duration = 4,
    battery_cubes = {
        "baseYear": 2023,
        "data": [
            { "duration": 2, "value": 198.463 },
            { "duration": 4, "value": 396.925 },
        ],
    },
    battery_ex_cubes = {
        "baseYear": 2023,
        "data": [
            { "duration": 2, "value": 41.572 },
            { "duration": 4, "value": 83.144 },
        ],
    },
    inflation_inputs = None,
    bess_capex_forecast = {
        "inflationProfile": "noInflation",
        "baseYear": 2023,
    },
    sensitivity = 0,
    operation_years = 40
):
    # inputData is not defined in the given JavaScript code
    # Assuming that it is globally defined
    inputData = 
    {
        "model": "Conservative",
        "data": [
            {
                "duration": 2,
                "data": [None]*28
            },
            {
                "duration": 4,
                "data": [
                    1850.08, 1863.288, 1836.851, 1768.061, 1699.272, 1630.484,
                    1561.697, 1492.911, 1482.69, 1472.468, 1462.246, 1452.025,
                    1441.803, 1431.581, 1421.36, 1411.138, 1400.917, 1390.695,
                    1380.473, 1370.252, 1360.03, 1349.808, 1339.587, 1329.365,
                    1319.143, 1308.922, 1289.7, 1288.478
                ]
            },
            {
                "duration": 8,
                "data": [None]*28
            }
        ]
    },
       {
        "model": "Moderate",
        "data": [
            {
                "duration": 2,
                "data": [
                    1022, 980, 862, 839, 817, 794, 771, 749, 739, 728, 718,
                    708, 697, 687, 677, 666, 656, 646, 635, 625, 615, 604,
                    594, 583, 573, 562, 552, 541
                ]
            },
            {
                "duration": 4,
                "data": [
                    1716, 1639, 1436, 1390, 1343, 1297, 1250, 1204, 1185,
                    1167, 1148, 1130, 1111, 1092, 1074, 1055, 1037, 1018,
                    1000, 981, 963, 944, 925, 907, 888, 870, 851, 833
                ]
            },
            {
                "duration": 8,
                "data": [
                    3102, 2956, 2584, 2490, 2396, 2302, 2208, 2114, 2079,
                    2044, 2008, 1973, 1938, 1903, 1868, 1833, 1798, 1763,
                    1728, 1693, 1658, 1624, 1589, 1554, 1519, 1484, 1450,
                    1415
                ]
            }
        ]
    },
    {
    "model": "Advanced",
    "data": [
        {
            "duration": 2,
            "data": [None]*28
        },
        {
            "duration": 4,
            "data": [
                1283, 1211, 1150, 1101, 1052, 1003, 955, 906, 890, 874,
                858, 842, 826, 810, 795, 779, 763, 747, 731, 715, 699,
                683, 668, 652, 636, 620, 604, 588
            ]
        },
        {
            "duration": 8,
            "data": [None]*28
        }
    ]
}
    selected_data = next((m for m in inputData if m.get('model') == model), None)

    # if(mode == 'Live selection')
    #     return selected_data
    # if(mode == 'Long-term profile - absolute'){
    #     // selectedData.map()
    #     return selected_data
    # }

    percentage_data = {
        "model": selected_data["model"],
        "data": [
            {
                "duration": d["duration"],
                "data": [
                    1 if index == 0 else round(dd / d["data"][0], 4)
                    for index, dd in enumerate(d["data"])
                ],
            }
            for d in selected_data["data"]
        ],
    }

    cubes_base_price = next((d["value"] for d in battery_cubes["data"] if d["duration"] == battery_duration), 0)
    cubes_ex_base_price = next((d["value"] for d in battery_ex_cubes["data"] if d["duration"] == battery_duration), 0)

    battery_cubes_forecast = [
        d * cubes_base_price
        for d in normalize_array(next((d["data"] for d in percentage_data["data"] if d["duration"] == battery_duration), []), operation_years + 5)
    ]

    battery_ex_cubes_forecast = [
        d * cubes_ex_base_price
        for d in normalize_array(next((d["data"] for d in percentage_data["data"] if d["duration"] == battery_duration), []), operation_years + 5)
    ]

    index_value = inflation_index(
        inflation_inputs,
        bess_capex_forecast["baseYear"],
        bess_capex_forecast["inflationProfile"]
    )

    annual_batteries_capex_forecast = [
        (b + battery_ex_cubes_forecast[index]) * normalize_array(index_value, operation_years + 5)[index] * (1 + sensitivity)
        for index, b in enumerate(battery_cubes_forecast)
    ]

    return [
        round_array(battery_cubes_forecast, 2),
        round_array(battery_ex_cubes_forecast, 2),
        round_array(annual_batteries_capex_forecast, 2),
    ]

def get_live_degradation_per_cycle(
    initial_cycle_data,
    starting_assumptions_for_batteries = {
        "degradationForecastAverageCyclesPerDay": 1.25,
        "batteryAvailability": 97,
        "batteryDuration": 4,
    }
):
    live_cycle_data = []
    degradation_per_cycle_data = get_degradation_per_cycle(initial_cycle_data)
    years = len(degradation_per_cycle_data[0]["degradationPerCycle"])

    if starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"] >= degradation_per_cycle_data[1]["averagePerCycle"]:
        a = degradation_per_cycle_data[0]["averagePerCycle"] - starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
        b = starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"] - degradation_per_cycle_data[1]["averagePerCycle"]

        for i in range(years):
            for k in range(12):
                live_cycle_data.append(
                    (b * degradation_per_cycle_data[0]["degradationPerCycle"][i] + a * degradation_per_cycle_data[1]["degradationPerCycle"][i]) / (a + b) / 365 / 100 / starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
                )
    else:
        c = degradation_per_cycle_data[1]["averagePerCycle"] - starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
        d = starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"] - degradation_per_cycle_data[2]["averagePerCycle"]

        for i in range(years):
            for k in range(12):
                live_cycle_data.append(
                    (d * degradation_per_cycle_data[1]["degradationPerCycle"][i] + c * degradation_per_cycle_data[2]["degradationPerCycle"][i]) / (c + d) / 365 / 100 / starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
                )

    return round_array(live_cycle_data, 10)

def getActiveScenarioRevenueItems(
    revenueSetup = {
        "forecastProviderChoice": "Modo",
        "inflation": "CPI to 2050 then nil",
        "baseYear": 2023,
    },
    assumptionsData = [
        {
            "providerName": "Modo",
            "data": {
                "efficiency": 88,
                "inflation": "FES to 2050 then nil",
                "baseYear": 2023,
                "region": "Northern",
                "tradingStrategy": "Merchant and ancillaries",
            },
        },
    ],
    startingAssumptionsForBatteries = {
        "degradationForecastAverageCyclesPerDay": 1.25,
        "batteryAvailability": 97,
        "batteryDuration": 4,
    },
    detailedRevenueData = None
):
    selectedAssumptionsData = next((item for item in assumptionsData if item.get("providerName") == revenueSetup.get('forecastProviderChoice')), None).get('data')
    activeScenario = next((item for item in detailedRevenueData if item.get("forecastProvider") == revenueSetup.get('forecastProviderChoice')), None).get('dataByBatteryDuration')
    activeScenario = next((item for item in activeScenario if item.get("duration") == startingAssumptionsForBatteries.get('batteryDuration')), None).get('dataByTradingStrategy')
    activeScenario = next((item for item in activeScenario if item.get("tradingStrategy") == selectedAssumptionsData.get('tradingStrategy')), None).get('dataByRegion')
    activeScenario = next((item for item in activeScenario if item.get("region") == selectedAssumptionsData.get('region')), None).get('dataByItems')
    
    return activeScenario

def calcInflationAdjustmentFactor(inflationInputs, providerInflationProfile, providerBaseYear, projectInflationProfile, projectBaseYear):
    providerInflationValue = inflation_index(inflationInputs, providerBaseYear, providerInflationProfile)
    projectInflatonValue = inflation_index(inflationInputs, projectBaseYear, projectInflationProfile)
    inflationAdjustmentFactor = [i/j for i, j in zip(projectInflatonValue, providerInflationValue)]
    len_inflation = len(inflationAdjustmentFactor)
    adjustedArray = []
    for i in range(len_inflation):
        if i >= 2:
            adjustedArray.append(inflationAdjustmentFactor[i])
    return [round(num, 10) for num in adjustedArray]
