# from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
# from math import pow

# def calc_number_of_days_in_month(model_start_date="2023-01-01", operation_end_date="2068-06-30"):
#     model_start_date = datetime.strptime(model_start_date, '%Y-%m-%d')
#     operation_end_date = datetime.strptime(operation_end_date, '%Y-%m-%d')


#     if model_start_date > operation_end_date:
#         model_start_date, operation_end_date = operation_end_date, model_start_date

#     days_in_months = []

#     while model_start_date < operation_end_date:
#         year = model_start_date.year
#         month = model_start_date.month
#         next_month = model_start_date + relativedelta(months=1)
#         days_in_month = (next_month - model_start_date).days

#         if model_start_date.day > 1:
#             days_in_month -= model_start_date.day - 1
#             model_start_date = model_start_date.replace(day=1)

#         if model_start_date.year == operation_end_date.year and model_start_date.month == operation_end_date.month and operation_end_date.day != (next_month - model_start_date).days:
#             days_in_month -= (next_month - model_start_date).days - operation_end_date.day

#         days_in_months.append(days_in_month)

#         model_start_date = model_start_date + relativedelta(months=1)

#     return days_in_months

# # def calc_number_of_days_in_month(model_start_date="2023-01-01", operation_start_date="2028-01-01", operation_years=40):
# #     model_start_date = datetime.strptime(model_start_date, '%Y-%m-%d')
# #     operation_start_date = datetime.strptime(operation_start_date, '%Y-%m-%d')
# #     operation_start_date = operation_start_date + relativedelta(years=operation_years)

# #     if model_start_date > operation_start_date:
# #         model_start_date, operation_start_date = operation_start_date, model_start_date

# #     days_in_months = []

# #     while model_start_date < operation_start_date:
# #         year = model_start_date.year
# #         month = model_start_date.month
# #         days_in_month = (datetime(year, month, 1) - datetime(year, month, 1)).days

# #         if model_start_date.day > 1:
# #             days_in_month -= model_start_date.day - 1
# #             model_start_date = model_start_date.replace(day=1)

# #         if model_start_date.year == operation_start_date.year and model_start_date.month == operation_start_date.month and operation_start_date.day != (datetime(year, month, 1) - datetime(year, month, 1)).days:
# #             days_in_month -= (datetime(year, month, 1) - datetime(year, month, 1)).days - operation_start_date.day

# #         days_in_months.append(days_in_month)

# #         model_start_date = model_start_date + relativedelta(months=1)

# #     return days_in_months

# # other functions go here

# def npv(rate, cashflows):
#     npv = 0
#     real_rate = pow(1 + rate, 1 / 12)
#     for i in range(len(cashflows)):
#         npv += cashflows[i] / pow(real_rate, i)
#     return npv

# def calc_irr(temp_npv, temp_discount_rate, cash_flow):
#     inc = 0.25
#     dec = -0.25
#     count = 1
#     while abs(temp_npv) > 0.01:
#         if temp_npv > 0:
#             temp_discount_rate = temp_discount_rate * (1 + inc / count)
#         else:
#             temp_discount_rate = temp_discount_rate * (1 + dec / count)

#         temp_npv = npv(temp_discount_rate, cash_flow)
#         count += 1

#     irr = temp_discount_rate
#     return irr

# def payback_period(cashflow, payback_start_date_month_number_from_valuation_date):
#     sum = 0
#     i = 0
#     while i <= payback_start_date_month_number_from_valuation_date:
#         sum += cashflow[i]
#         i += 1
#     while sum < 0:
#         sum += cashflow[i]
#         i += 1

#     payback_period = (i + 1) / 12
#     return payback_period

# def get_operations_as_a_percent_of_period(model_start_date="2023-01-01", operation_start_date="2028-01-01", operation_years=40):
#     model_start_date = datetime.strptime(model_start_date, '%Y-%m-%d')
#     operation_start_date = datetime.strptime(operation_start_date, '%Y-%m-%d')
#     operation_start_date = operation_start_date + relativedelta(years=operation_years)

#     if model_start_date > operation_start_date:
#         model_start_date, operation_start_date = operation_start_date, model_start_date

#     values = []

#     while model_start_date < operation_start_date:
#         if model_start_date <= operation_start_date - relativedelta(years=operation_years):
#             values.append(0)
#         else:
#             values.append(1)
#         model_start_date = model_start_date + relativedelta(months=1)

#     return values

# def get_operations_as_a_percent_of_period(model_start_date="2023-01-01", operation_start_date="2028-01-01", operation_end_date="2068-01-01"):
#     model_start_date = datetime.strptime(model_start_date, '%Y-%m-%d')
#     operation_start_date = datetime.strptime(operation_start_date, '%Y-%m-%d')
#     operation_end_date = datetime.strptime(operation_end_date, '%Y-%m-%d')

#     if model_start_date > operation_start_date:
#         model_start_date, operation_start_date = operation_start_date, model_start_date

#     values = []

#     while model_start_date < operation_end_date:
#         if model_start_date < operation_start_date:
#             values.append(0)
#         else:
#             values.append(1)
#         model_start_date = model_start_date + relativedelta(months=1)

#     return values
# # def 	(date1="2023-01-01", date2="2068-06-30"):
# #     date1 = datetime.strptime(date1, '%Y-%m-%d').replace(day=1)
# #     date2 = datetime.strptime(date2, '%Y-%m-%d').replace(day=1)

# #     if date1 > date2:
# #         date1, date2 = date2, date1

# #     years = date2.year - date1.year
# #     months = date2.month - date1.month

# #     month_number_from_model_start_date = years * 12 + months + 1

# #     return month_number_from_model_start_date


# def get_as_a_percent_of_period(start_date, date1, date2, end_date):
#     arr = []
#     start_date = datetime.strptime(start_date, '%Y-%m-%d')
#     date1 = datetime.strptime(date1, '%Y-%m-%d')
#     date2 = datetime.strptime(date2, '%Y-%m-%d')
#     end_date = datetime.strptime(end_date, '%Y-%m-%d')

#     while start_date <= end_date:
#         if date1 <= start_date <= date2:
#             arr.append(1)
#         else:
#             arr.append(0)
#         start_date = start_date + relativedelta(months=1)

#     return arr

# def calc_days_in_month(model_start_date = "2023-01-01", operation_end_date = "2024-01-01"):
#     # Convert strings to Date objects
#     model_start_date = datetime.strptime(model_start_date, '%Y-%m-%d')
#     operation_end_date = datetime.strptime(operation_end_date, '%Y-%m-%d')

#     # Ensure model_start_date is the earlier date
#     if model_start_date > operation_end_date:
#         temp = model_start_date
#         model_start_date = operation_end_date
#         operation_end_date = temp

#     days_in_months = []

#     while True:
#         year = model_start_date.year
#         month = model_start_date.month
#         days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day  # Get last day of month

#         # If it's the first month, subtract the starting day
#         if model_start_date.day > 1:
#             days_in_month -= model_start_date.day - 1
#             model_start_date = model_start_date.replace(day=1)  # Set to the first day of the month

#         # If it's the last month and not the last day of the month, subtract the remaining days
#         if model_start_date.year == operation_end_date.year and model_start_date.month == operation_end_date.month:
#             days_in_month -= (datetime(year, month + 1, 1) - timedelta(days=1)).day - operation_end_date.day

#             days_in_months.append(days_in_month)
#             break

#         days_in_months.append(days_in_month)
#         model_start_date += relativedelta(months=1)  # Go to the next month

#     return days_in_months

# def calc_period():
#     period = get_months_number_from_model_start_date() - 1
#     return period



# def yearly_flag(arr, start_date):
#     start_month = datetime.strptime(start_date, '%Y-%m-%d').month
#     sum_arr = []
#     sum = 0

#     for i in range(len(arr)):
#         if i < 12 - start_month:
#             sum += arr[i]
#             if i == 11 - start_month:
#                 if sum > 0: 
#                     sum_arr.append(1)
#                 else: 
#                     sum_arr.append(0)
#                 sum = 0
#         else:
#             sum += arr[i]
#             if (i - (11 - start_month)) % 12 == 0:
#                 if sum > 0: 
#                     sum_arr.append(1)
#                 else: 
#                     sum_arr.append(0)
#                 sum = 0
#             elif i == len(arr) - 1:
#                 if sum > 0: 
#                     sum_arr.append(1)
#                 else: 
#                     sum_arr.append(0)

#     return sum_arr

# import math

# def normalize_array(array, length, default_value=None):
#     array_length = len(array)
#     _d = default_value or array[array_length - 1]
#     array += [_d] * (length - array_length)
#     array = array[:length]
#     return array

# def normalize_array_by_seasonality(array, length):
#     array_length = len(array)
#     for i in range(array_length, length):
#         array.append(array[i - 12])
#     return array

# def round_array(value, num_digits):
#     return [round(d, num_digits) for d in value]

# def array_divide(array1, array2):
#     return [d / array2[i] for i, d in enumerate(array1)]

# def round_number(value, num_digits):
#     return round(value, num_digits)

# def cumulative_multiply(array):
#     array_length = len(array)
#     value = []
#     for i in range(array_length):
#         if i == 0:
#             value.append(1)
#         else:
#             value.append(value[i - 1] * (1 + array[i] / 100))
#     return value

# def annual_index_to_months(array):
#     len_array = len(array)
#     result_array = []
#     for i in range(len_array):
#         for j in range(12):
#             result_array.append(array[i])
#     return result_array

# from datetime import datetime, timedelta
# from operator import mul
# from functools import reduce

# def add_years(date_string, years):
#     date = datetime.strptime(date_string, '%Y-%m-%d')
#     date = date.replace(year=date.year + years)
#     return date.strftime('%Y-%m-%d')

# def array_sum(array_1, array_2):
#     return [d + array_2[i] for i, d in enumerate(array_1)]

# def add_zeros(array, length):
#     array += [0] * (length - len(array))
#     return array[:length]

# def sum_monthly_values(arr, start_date):
#     start_month = datetime.strptime(start_date, '%Y-%m-%d').month
#     sum_arr = []
#     sum = 0

#     for i in range(len(arr)):
#         if i < 12 - start_month:
#             sum += arr[i]
#             if i == 11 - start_month:
#                 sum_arr.append(sum)
#                 sum = 0
#         else:
#             sum += arr[i]
#             if (i - (11 - start_month)) % 12 == 0:
#                 sum_arr.append(sum)
#                 sum = 0
#             elif i == len(arr) - 1:
#                 sum_arr.append(sum)

#     return sum_arr

# def expand_and_average(arr, num):
#     arr += [0] * num
#     averages = [sum(arr[i + 1:i + num + 1]) / num for i in range(len(arr) - num)]
#     return averages

# def sum_arrays(*arrays):
#     return [sum(values) for values in zip(*arrays)]

# def multiply_number(array, num):
#     return [i * num for i in array]

# def nth_largest(arr, n):
#     indexed_arr = sorted([(e, i) for i, e in enumerate(arr)], reverse=True)
#     return indexed_arr[n - 1]

# def multiply_arrays(*arrays):
#     return [reduce(mul, values) for values in zip(*arrays)]

# def sum_array(arr):
#     return sum(arr)

# def expand_and_sum(arr, num):
#     arr_copy = arr + [0] * num
#     sums = [sum(arr_copy[i:i + num]) for i in range(len(arr_copy) - num)]
#     return sums

# def min_array(*arrays):
#     return [min(values) for values in zip(*arrays)]
# def sum_array(arr):
#     return sum(arr)

# from datetime import datetime

# def getMonthsNumberFromModelStartDate(date1 = "2023-01-01", date2 = "2068-06-30"):
#     # Convert strings to datetime objects
#     date1 = datetime.strptime(date1, "%Y-%m-%d")
#     date2 = datetime.strptime(date2, "%Y-%m-%d")

#     # Ensure date1 is the earlier date
#     if date1 > date2:
#         temp = date1
#         date1 = date2
#         date2 = temp

#     years = date2.year - date1.year
#     months = date2.month - date1.month

#     # Calculate total months
#     monthNumberFromModelStartDate = years * 12 + months + 1

#     return monthNumberFromModelStartDate+1

# def inflation_index(inflation_inputs, base_year=2023, profile="CPI to 2050 then nil"):
#     match_data = next(item for item in getInflationIndex(inflation_inputs) if item["profile"] == profile)["rate"]
#     inflation_result = []

#     base_value = match_data[base_year - 2021]
#     inflation_result = [m / base_value for m in match_data]
#     return inflation_result

# def getInflationIndex(inflationInputs):
#     inflationIndex = []
#     for d in inflationInputs:
#         inflationIndex.append({
#             'profile': d['profile'],
#             'rate': round_array(cumulative_multiply(d['rate']), 10)
#         })
#     return inflationIndex

# def get_cycles_per_month(
#     revenue_setup = {
#         "forecastProviderChoice": "Modo",
#         "inflation": "CPI to 2050 then nil",
#         "baseYear": 2023,
#     },
#     assumptions_data = [
#         {
#             "providerName": "Modo",
#             "data": {
#                 "efficiency": 88,
#                 "inflation": "FES to 2050 then nil",
#                 "baseYear": 2023,
#                 "region": "Nothern",
#                 "tradingStrategy": "Merchant and ancillaries",
#             },
#         },
#     ],
#     starting_assumptions_for_batteries = {
#         "degradationForecastAverageCyclesPerDay": 1.25,
#         "batteryAvailability": 97,
#         "batteryDuration": 4,
#     },
#     detailed_revenue_data = None,
#     model_start_date = "2023-01-01",
#     operation_start_date = "2028-01-01",
#     decommissioningEndDate = "2068-06-30",
#     operation_years = 40
# ):
#     number_of_days_in_month = calc_number_of_days_in_month(
#         model_start_date,
#         decommissioningEndDate
#     )
#     cycles_per_day = next((d for d in getActiveScenarioRevenueItems(
#         revenue_setup,
#         assumptions_data,
#         starting_assumptions_for_batteries,
#         detailed_revenue_data
#     ) if d.get('item') == "Avg. Cycles per day"), {}).get('data')

#     operations_as_a_percent_of_period = get_operations_as_a_percent_of_period(
#         model_start_date,
#         operation_start_date,
#         operation_years
#     )
#     print(len(number_of_days_in_month),len(cycles_per_day),len(operations_as_a_percent_of_period))
    
#     average_cycles_per_month = [
#         round(
#             d * cycles_per_day[i] * operations_as_a_percent_of_period[i], 3
#         ) for i, d in enumerate(number_of_days_in_month)
#     ]
#     return average_cycles_per_month

# def calc_capex_forecast(
#     model = "Conservative",
#     battery_duration = 4,
#     battery_cubes = {
#         "baseYear": 2023,
#         "data": [
#             { "duration": 2, "value": 198.463 },
#             { "duration": 4, "value": 396.925 },
#         ],
#     },
#     battery_ex_cubes = {
#         "baseYear": 2023,
#         "data": [
#             { "duration": 2, "value": 41.572 },
#             { "duration": 4, "value": 83.144 },
#         ],
#     },
#     inflation_inputs = None,
#     bess_capex_forecast = {
#         "inflationProfile": "noInflation",
#         "baseYear": 2023,
#     },
#     sensitivity = 0,
#     operation_years = 40
# ):
#     # inputData is not defined in the given JavaScript code
#     # Assuming that it is globally defined
#     inputData = {
#         "model": "Conservative",
#         "data": [
#             {
#                 "duration": 2,
#                 "data": [None]*28
#             },
#             {
#                 "duration": 4,
#                 "data": [
#                     1850.08, 1863.288, 1836.851, 1768.061, 1699.272, 1630.484,
#                     1561.697, 1492.911, 1482.69, 1472.468, 1462.246, 1452.025,
#                     1441.803, 1431.581, 1421.36, 1411.138, 1400.917, 1390.695,
#                     1380.473, 1370.252, 1360.03, 1349.808, 1339.587, 1329.365,
#                     1319.143, 1308.922, 1289.7, 1288.478
#                 ]
#             },
#             {
#                 "duration": 8,
#                 "data": [None]*28
#             }
#         ]
#     },
#     {
#         "model": "Moderate",
#         "data": [
#             {
#                 "duration": 2,
#                 "data": [
#                     1022, 980, 862, 839, 817, 794, 771, 749, 739, 728, 718,
#                     708, 697, 687, 677, 666, 656, 646, 635, 625, 615, 604,
#                     594, 583, 573, 562, 552, 541
#                 ]
#             },
#             {
#                 "duration": 4,
#                 "data": [
#                     1716, 1639, 1436, 1390, 1343, 1297, 1250, 1204, 1185,
#                     1167, 1148, 1130, 1111, 1092, 1074, 1055, 1037, 1018,
#                     1000, 981, 963, 944, 925, 907, 888, 870, 851, 833
#                 ]
#             },
#             {
#                 "duration": 8,
#                 "data": [
#                     3102, 2956, 2584, 2490, 2396, 2302, 2208, 2114, 2079,
#                     2044, 2008, 1973, 1938, 1903, 1868, 1833, 1798, 1763,
#                     1728, 1693, 1658, 1624, 1589, 1554, 1519, 1484, 1450,
#                     1415
#                 ]
#             }
#         ]
#     },
#     {
#     "model": "Advanced",
#     "data": [
#         {
#             "duration": 2,
#             "data": [None]*28
#         },
#         {
#             "duration": 4,
#             "data": [
#                 1283, 1211, 1150, 1101, 1052, 1003, 955, 906, 890, 874,
#                 858, 842, 826, 810, 795, 779, 763, 747, 731, 715, 699,
#                 683, 668, 652, 636, 620, 604, 588
#             ]
#         },
#         {
#             "duration": 8,
#             "data": [None]*28
#         }
#     ]
# }
#     selected_data = next((m for m in inputData if m.get('model') == model), None)

#     # if(mode == 'Live selection')
#     #     return selected_data
#     # if(mode == 'Long-term profile - absolute'){
#     #     // selectedData.map()
#     #     return selected_data
#     # }

#     print(selected_data)
#     percentage_data = {
#         "model": selected_data["model"],
#         "data": [
#             {
#                 "duration": d["duration"],
#                 "data": [
#                     1 if index == 0 else 0 if dd == None or d["data"][0] == None else round(dd / d["data"][0], 4)
#                     for index, dd in enumerate(d["data"])
#                 ],
#             }
#             for d in selected_data["data"]
#         ],
#     }

#     cubes_base_price = next((d["value"] for d in battery_cubes["data"] if d["duration"] == battery_duration), 0)
#     cubes_ex_base_price = next((d["value"] for d in battery_ex_cubes["data"] if d["duration"] == battery_duration), 0)

#     battery_cubes_forecast = [
#         d * cubes_base_price
#         for d in normalize_array(next((d["data"] for d in percentage_data["data"] if d["duration"] == battery_duration), []), operation_years + 5)
#     ]

#     battery_ex_cubes_forecast = [
#         d * cubes_ex_base_price
#         for d in normalize_array(next((d["data"] for d in percentage_data["data"] if d["duration"] == battery_duration), []), operation_years + 5)
#     ]

#     index_value = inflation_index(
#         inflation_inputs,
#         bess_capex_forecast["baseYear"],
#         bess_capex_forecast["inflationProfile"]
#     )

#     annual_batteries_capex_forecast = [
#         (b + battery_ex_cubes_forecast[index]) * normalize_array(index_value, operation_years + 5)[index] * (1 + sensitivity)
#         for index, b in enumerate(battery_cubes_forecast)
#     ]

#     return [
#         round_array(battery_cubes_forecast, 2),
#         round_array(battery_ex_cubes_forecast, 2),
#         round_array(annual_batteries_capex_forecast, 2),
#     ]

# def get_degradation_per_cycle(initialCycleData):
#     ceilingCycle = initialCycleData[0]['averageCyclesPerDay']
#     middleCycle = initialCycleData[1]['averageCyclesPerDay']
#     floorCycle = initialCycleData[2]['averageCyclesPerDay']

#     ceilingRetentionRate = initialCycleData[0]['retentionRate']
#     middleRetentionRate = initialCycleData[1]['retentionRate']
#     floorRetentionRate = initialCycleData[2]['retentionRate']

#     ceilingDegradationPerCycle = []
#     middleDegradationPerCycle = []
#     floorDegradationPerCycle = []
#     years = len(ceilingRetentionRate)

#     for i in range(years):
#         if i == 0:
#             ceilingDegradationPerCycle.append(100 - ceilingRetentionRate[i])
#             middleDegradationPerCycle.append(100 - middleRetentionRate[i])
#             floorDegradationPerCycle.append(100 - floorRetentionRate[i])
#         else:
#             ceilingDegradationPerCycle.append(ceilingRetentionRate[i - 1] - ceilingRetentionRate[i])
#             middleDegradationPerCycle.append(middleRetentionRate[i - 1] - middleRetentionRate[i])
#             floorDegradationPerCycle.append(floorRetentionRate[i - 1] - floorRetentionRate[i])

#     degradationPerCycleData = [
#         {
#             'averagePerCycle': ceilingCycle,
#             'degradationPerCycle': ceilingDegradationPerCycle,
#         },
#         {
#             'averagePerCycle': middleCycle,
#             'degradationPerCycle': middleDegradationPerCycle,
#         },
#         {
#             'averagePerCycle': floorCycle,
#             'degradationPerCycle': floorDegradationPerCycle,
#         },
#     ]

#     return degradationPerCycleData

# def get_live_degradation_per_cycle(
#     initial_cycle_data,
#     starting_assumptions_for_batteries = {
#         "degradationForecastAverageCyclesPerDay": 1.25,
#         "batteryAvailability": 97,
#         "batteryDuration": 4,
#     }
# ):
#     live_cycle_data = []
#     degradation_per_cycle_data = get_degradation_per_cycle(initial_cycle_data)
#     years = len(degradation_per_cycle_data[0]["degradationPerCycle"])

#     if starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"] >= degradation_per_cycle_data[1]["averagePerCycle"]:
#         a = degradation_per_cycle_data[0]["averagePerCycle"] - starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
#         b = starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"] - degradation_per_cycle_data[1]["averagePerCycle"]

#         for i in range(years):
#             for k in range(12):
#                 live_cycle_data.append(
#                     (b * degradation_per_cycle_data[0]["degradationPerCycle"][i] + a * degradation_per_cycle_data[1]["degradationPerCycle"][i]) / (a + b) / 365 / 100 / starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
#                 )
#     else:
#         c = degradation_per_cycle_data[1]["averagePerCycle"] - starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
#         d = starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"] - degradation_per_cycle_data[2]["averagePerCycle"]

#         for i in range(years):
#             for k in range(12):
#                 live_cycle_data.append(
#                     (d * degradation_per_cycle_data[1]["degradationPerCycle"][i] + c * degradation_per_cycle_data[2]["degradationPerCycle"][i]) / (c + d) / 365 / 100 / starting_assumptions_for_batteries["degradationForecastAverageCyclesPerDay"]
#                 )

#     return round_array(live_cycle_data, 10)

# def getActiveScenarioRevenueItems(
#     revenueSetup = {
#         "forecastProviderChoice": "Modo",
#         "inflation": "CPI to 2050 then nil",
#         "baseYear": 2023,
#     },
#     assumptionsData = [
#         {
#             "providerName": "Modo",
#             "data": {
#                 "efficiency": 88,
#                 "inflation": "FES to 2050 then nil",
#                 "baseYear": 2023,
#                 "region": "Nothern",
#                 "tradingStrategy": "Merchant and ancillaries",
#             },
#         },
#     ],
#     startingAssumptionsForBatteries = {
#         "degradationForecastAverageCyclesPerDay": 1.25,
#         "batteryAvailability": 97,
#         "batteryDuration": 4,
#     },
#     detailedRevenueData = []
# ):
#     selectedAssumptionsData = next((item for item in assumptionsData if item.get("providerName") == revenueSetup.get('forecastProviderChoice')), None).get('data')
#     activeScenario = next((item for item in detailedRevenueData if item.get("forecastProvider") == revenueSetup.get('forecastProviderChoice')), None).get('dataByBatteryDuration')
#     activeScenario = next((item for item in activeScenario if item.get("dataByBatteryDuration") == startingAssumptionsForBatteries.get('batteryDuration')), None).get('dataByTradingStrategy')
#     activeScenario = next((item for item in activeScenario if item.get("tradingStrategy") == selectedAssumptionsData.get('tradingStrategy')), None).get('dataByRegion')
#     activeScenario = next((item for item in activeScenario if item.get("region") == selectedAssumptionsData.get('region')), None).get('dataByItems')
    
#     return activeScenario

# def calcInflationAdjustmentFactor(inflationInputs, providerInflationProfile, providerBaseYear, projectInflationProfile, projectBaseYear):
#     providerInflationValue = inflation_index(inflationInputs, providerBaseYear, providerInflationProfile)
#     projectInflatonValue = inflation_index(inflationInputs, projectBaseYear, projectInflationProfile)
#     inflationAdjustmentFactor = [i/j for i, j in zip(projectInflatonValue, providerInflationValue)]
#     len_inflation = len(inflationAdjustmentFactor)
#     adjustedArray = []
#     for i in range(len_inflation):
#         if i >= 2:
#             adjustedArray.append(inflationAdjustmentFactor[i])
#     return [round(num, 10) for num in adjustedArray]
