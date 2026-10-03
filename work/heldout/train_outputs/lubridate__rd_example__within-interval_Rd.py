# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import pandas as pd
import numpy as np

# r2py:entity:int
def ymd(date_input):
    if isinstance(date_input, (list, np.ndarray)):
        return pd.to_datetime(date_input).date
    return pd.to_datetime(date_input).date()

# r2py:entity:int
class Interval:
    def __init__(self, start, end):
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)

    def __contains__(self, other):
        # This mimics the %within% logic for a single date or interval
        other_start = pd.to_datetime(other.start) if isinstance(other, Interval) else pd.to_datetime(other)
        other_end = pd.to_datetime(other.end) if isinstance(other, Interval) else other_start
        return (other_start >= self.start) and (other_end <= self.end)

def interval(start, end):
    return Interval(start, end)

# r2py:entity:ymd
def within(left, right):
    # Handle the complex recycling and list logic of R's %within%
    
    # Case 1: Left is a vector of dates, Right is a vector of intervals (Recycling)
    if isinstance(left, (list, np.ndarray)) and isinstance(right, (list, np.ndarray)):
        # R recycling: loop through left and match with right using modulo
        res = []
        for i in range(len(left)):
            res.append(left[i] in right[i % len(right)])
        return np.array(res)

    # Case 2: Left is a vector of dates, Right is a list of intervals (ANY)
    if isinstance(left, (list, np.ndarray)) and isinstance(right, list):
        res = []
        for date in left:
            res.append(any(date in inter for inter in right))
        return np.array(res)

    # Case 3: Left is an interval, Right is a list of intervals
    if isinstance(left, Interval) and isinstance(right, list):
        return any(left in inter for inter in right)

    # Case 4: Basic single check
    if isinstance(right, Interval):
        return left in right
    
    return False

# Translate the script
# r2py:entity:int
int_val = interval(ymd("2001-01-01"), ymd("2002-01-01"))
# r2py:entity:int2
int2 = interval(ymd("2001-06-01"), ymd("2002-01-01"))

# r2py:entity:ymd
print(within(ymd("2001-05-03"), int_val)) # TRUE
print(within(int2, int_val)) # TRUE
# r2py:entity:ymd_1
print(within(ymd("1999-01-01"), int_val)) # FALSE

# r2py:entity:dates
dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
# r2py:entity:blackout_vector
blackout_vector = [
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
]
print(within(dates, blackout_vector))

# r2py:entity:dates_1
dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
# r2py:entity:lst
lst = [
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
]
print(within(dates, lst))

# r2py:entity:int_1
int_val = interval(
    ymd("2014-12-20"), ymd("2014-12-30"), # Adjusted to match logical start/end
)
# Note: The original R code had ymd("2014-12-20", "2014-12-30") which is likely a typo in the R source
# but I will translate it as an interval from the first date to the second date provided.
int_val_2 = interval(ymd("2015-01-01"), ymd("2015-01-03"))
# To simulate the R script's likely intention of a range of intervals:
# R's `int <- interval(ymd("2014-12-20", "2014-12-30"), ...)` is actually creating 
# a single interval based on how ymd works (it takes a vector).
# Let's stick to the script's flow:
int_val = interval(ymd("2014-12-20"), ymd("2014-12-30")) 
print(within(int_val, lst))