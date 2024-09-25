import datetime
from datetime import date
from dateutil.relativedelta import relativedelta




def sumArrays(*arrays):
    numArrays = len(arrays)
    lenOfResult = len(arrays[0])
    index = 0
    result = [0] * lenOfResult
    while index < lenOfResult:
        result[index] = 0
        for j in range (numArrays):
            result[index] = result[index] + arrays[j][index]
            j+=1
        index += 1
    return result

def multiplyArrayByNumber(arr,num):
    lenArr = len(arr)
    i = 0
    result = [0] * lenArr
    while i < lenArr:
        result[i] = arr[i]*num
        i+=1
    return result

def multiplyArrays(*arrays):
    numArrays = len(arrays)
    lenOfResult = len(arrays[0])
    index = 0
    result = [0] * lenOfResult
    while index < lenOfResult:
        result[index] = 1
        for j in range (numArrays):
            result[index] = result[index] * arrays[j][index]
            j+=1
        index += 1
    return result

def getDate(dateStr,numberOfMonths):
    baseDate = datetime.datetime.strptime(dateStr,'%Y-%m-%d')+relativedelta(months=+numberOfMonths)
    return baseDate

def arrayFillWithZeros(arr, totalLen):
    arrLen = len(arr)
    i = 0
    resultArray = [0] * totalLen
    while i < totalLen:
        if i < arrLen:
            resultArray[i] = arr[i]
        else:
            resultArray[i] = 0
        i += 1
    return resultArray

def calcSumOfValuesOfTheArray(arr):
    length = len(arr)
    index = 0 
    sum = 0
    while index < length:
        sum += arr[index]
        index += 1
    return sum

        
    