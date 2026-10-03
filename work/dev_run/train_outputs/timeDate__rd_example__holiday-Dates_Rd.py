# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import datetime
import numpy as np
from dateutil.relativedelta import relativedelta, MO

def getRmetricsOptions(x=None, unset=""):
    # Mocking the Rmetrics global options environment
    # In a real scenario, currentYear is typically the current calendar year
    options = {"currentYear": datetime.datetime.now().year}
    if x is None:
        return options
    return options.get(x, unset)

def timeDate(charvec, format_val=None, zone="", FinCenter=""):
    # The R timeDate function is a generic for casting/formatting dates
    # For the purpose of these examples, it returns the date representation
    if isinstance(charvec, (list, np.ndarray)):
        return [str(x) for x in charvec]
    return str(charvec)

def Easter(year=None, shift=0):
    if year is None:
        year = getRmetricsOptions("currentYear")
    
    # Support for arrays of years
    years = np.atleast_1d(year)
    results = []
    
    for y in years:
        a = y % 19
        b = y // 100
        c = y % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        
        dt = datetime.date(y, month, day) + relativedelta(days=shift)
        results.append(dt)
    
    if np.isscalar(year):
        return results[0]
    return np.array(results)

# r2py:entity:CHSechselaeuten
def _nth_of_nday(year, month, day_of_week, nth):
    # R: .nth.of.nday(y, 4, 1, 3) -> 3rd Monday (1) of April (4)
    # Python dateutil: MO(3) for 3rd Monday
    first_of_month = datetime.date(year, month, 1)
    # weekday 0=Monday in python
    target_day = first_of_month + relativedelta(weekday=MO(nth))
    # If the 1st is a Tuesday, MO(1) might jump to the next week. 
    # But if 1st is Monday, MO(1) is the 1st. 
    # dateutil's MO(nth) works correctly from the start of the month.
    if target_day.month != month:
        # This handles cases where the date might wrap, though rare for nth of month
        pass
    return target_day

def CHSechselaeuten(year=None, value="timeDate", na_drop=True):
    if year is None:
        year = getRmetricsOptions("currentYear")
    
    years = np.atleast_1d(year)
    ans = []
    for y in years:
        # 3rd Monday of April
        theDate = _nth_of_nday(y, 4, 0, 3)
        # If 3rd Monday is Easter Monday (Easter Sunday + 1), move to 4th Monday
        if theDate == Easter(y, shift=1):
            theDate = _nth_of_nday(y, 4, 0, 4)
        ans.append(theDate)
    
    if value == "timeDate":
        return [d.strftime("%Y-%m-%d") for d in ans] if not np.isscalar(year) else ans[0].strftime("%Y-%m-%d")
    return ans

# r2py:entity:DEGermanUnity
def DEGermanUnity(year=None, value="timeDate", na_drop=True):
    if year is None:
        year = getRmetricsOptions("currentYear")
    
    years = np.atleast_1d(year)
    ans = []
    for y in years:
        # German Unity Day is October 3rd
        ans.append(datetime.date(y, 10, 3))
    
    if value == "timeDate":
        return [d.strftime("%Y-%m-%d") for d in ans] if not np.isscalar(year) else ans[0].strftime("%Y-%m-%d")
    return ans

# Execution
# r2py:entity:CHSechselaeuten
years_range = np.arange(2000, 2011)
print(CHSechselaeuten(years_range))
# r2py:entity:CHSechselaeuten_1
print(CHSechselaeuten(getRmetricsOptions("currentYear")))

# r2py:entity:DEGermanUnity
print(DEGermanUnity(getRmetricsOptions("currentYear")))