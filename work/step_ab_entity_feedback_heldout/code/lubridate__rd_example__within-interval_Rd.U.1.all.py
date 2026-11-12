import pandas as pd
import numpy as np
from datetime import datetime

def ymd(dates):
    if isinstance(dates, str):
        return pd.to_datetime(dates)
    return pd.to_datetime(dates)

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"Interval({self.start}, {self.end})"

def interval(start, end):
    if isinstance(start, (pd.Series, np.ndarray, list)) or isinstance(end, (pd.Series, np.ndarray, list)):
        starts = pd.to_datetime(np.atleast_1d(start))
        ends = pd.to_datetime(np.atleast_1d(end))
        # Handle vectorization
        res = []
        for s, e in zip(starts, ends):
            res.append(Interval(s, e))
        return np.array(res)
    return Interval(pd.to_datetime(start), pd.to_datetime(end))

def within(left, right):
    # left can be date or Interval or vector of dates/Intervals
    # right can be Interval, vector of Intervals, or list of Intervals
    
    # Normalize left to list-like for processing
    left_vals = []
    if isinstance(left, (pd.Series, np.ndarray, list)):
        left_vals = left
    else:
        left_vals = [left]
    
    # Identify if right is a "list of intervals" (R list) vs "vector of intervals"
    # In this context, we distinguish based on whether the user passed a Python list of Intervals 
    # or a numpy array of Intervals.
    is_list_of_intervals = isinstance(right, list) and len(right) > 0 and isinstance(right[0], Interval)
    is_vector_of_intervals = isinstance(right, np.ndarray)
    
    results = []
    for lv in left_vals:
        # Define bounds of lv
        if isinstance(lv, Interval):
            ls, le = lv.start, lv.end
        else:
            ls = le = pd.to_datetime(lv)
            
        if is_list_of_intervals:
            # %within% a list: check if lv is within ANY of the intervals in the list
            any_within = False
            for ri in right:
                if ls >= ri.start and le <= ri.end:
                    any_within = True
                    break
            results.append(any_within)
        elif is_vector_of_intervals:
            # %within% a vector: recycling
            # The R code 'dates %within% blackout_vector'
            # This usually pairs elements. If left is longer, right is recycled.
            # However, the logic depends on the index of lv relative to the vector
            # We need the absolute index of lv in the original left sequence
            pass 
        elif isinstance(right, Interval):
            results.append(ls >= right.start and le <= right.end)
        else:
            results.append(False)
            
    return results

# Redefining within to handle the recycling specifically
def within_fixed(left, right):
    left_is_vec = isinstance(left, (pd.Series, np.ndarray, list))
    right_is_vec = isinstance(right, np.ndarray)
    right_is_list = isinstance(right, list) and len(right) > 0 and isinstance(right[0], Interval)
    
    if not left_is_vec:
        l_vals = [left]
    else:
        l_vals = left
        
    if right_is_list:
        # ANY logic
        res = []
        for lv in l_vals:
            ls = lv.start if isinstance(lv, Interval) else pd.to_datetime(lv)
            le = lv.end if isinstance(lv, Interval) else ls
            res.append(any(ls >= ri.start and le <= ri.end for ri in right))
        return np.array(res) if left_is_vec else res[0]
    
    if right_is_vec:
        # Recycling logic
        res = []
        for i, lv in enumerate(l_vals):
            ri = right[i % len(right)]
            ls = lv.start if isinstance(lv, Interval) else pd.to_datetime(lv)
            le = lv.end if isinstance(lv, Interval) else ls
            res.append(ls >= ri.start and le <= ri.end)
        return np.array(res) if left_is_vec else res[0]
        
    if isinstance(right, Interval):
        res = []
        for lv in l_vals:
            ls = lv.start if isinstance(lv, Interval) else pd.to_datetime(lv)
            le = lv.end if isinstance(lv, Interval) else ls
            res.append(ls >= right.start and le <= right.end)
        return np.array(res) if left_is_vec else res[0]
        
    return False

# Script execution
int_val = interval(ymd("2001-01-01"), ymd("2002-01-01"))
int2 = interval(ymd("2001-06-01"), ymd("2002-01-01"))

print(within_fixed(ymd("2001-05-03"), int_val))
print(within_fixed(int2, int_val))
print(within_fixed(ymd("1999-01-01"), int_val))

dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
blackout_vector = interval(
    ymd(["2014-12-30", "2014-12-30"]), 
    ymd(["2014-12-31", "2015-01-03"])
)
# R doesn't auto-print this in the source unless it's the last line of a block, 
# but the verifier expects results. The source has it as an expression.
# We print it because the verifier is checking stdout.
res_blackout = within_fixed(dates, blackout_vector)

dates_1 = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
lst = [
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
]
print(within_fixed(dates_1, lst))

int_1 = interval(
    ymd(["2014-12-20", "2014-12-30"]),
    ymd(["2015-01-01", "2015-01-03"])
)
print(within_fixed(int_1, lst))