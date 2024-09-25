import app.api.utils.calcFunctions.basicAssumptions as inp
import app.api.utils.calcFunctions.basicResults as basResult
from app.api.utils.calcFunctions.basicFun import multiplyArrayByNumber

decommissioningCostPerPeriod = multiplyArrayByNumber(basResult.decommissioning_periodFlag,inp.decommissioning_total_cost)
