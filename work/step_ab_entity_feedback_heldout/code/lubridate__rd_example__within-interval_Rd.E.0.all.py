import pandas as pd
import numpy as np

def ymd(date_input, *args):
    # Handle both single string and multiple arguments (vectorized)
    inputs = []
    if isinstance(date_input, (list, np.ndarray)):
        inputs = date_input
    else:
        inputs = [date_input] + list(args)
    
    return pd.to_datetime(inputs)

class Interval:
    def __init__(self, start, end):
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)

    def __repr__(self):
        return f"Interval({self.start}, {self.end})"

def interval(start, end):
    # R's interval() can be vectorized if start/end are vectors
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    
    if isinstance(start_dt, pd.DatetimeIndex) or isinstance(end_dt, pd.DatetimeIndex):
        # Return a list/array of Interval objects
        s_vals = start_dt if isinstance(start_dt, pd.DatetimeIndex) else [start_dt] * len(end_dt)
        e_vals = end_dt if isinstance(end_dt, pd.DatetimeIndex) else [end_dt] * len(start_dt)
        return np.array([Interval(s, e) for s, e in zip(s_vals, e_vals)])
    else:
        return Interval(start_dt, end_dt)

def within(left, right):
    # Logic for %within%
    
    # Helper to check if a single date or interval is within a single interval
    def is_within(l, r):
        if not isinstance(r, Interval): return False
        l_start = pd.to_datetime(l.start) if isinstance(l, Interval) else pd.to_datetime(l)
        l_end = pd.to_datetime(l.end) if isinstance(l, Interval) else l_start
        return (l_start >= r.start) and (l_end <= r.end)

    # Case: Right is a list of intervals (Check if within ANY)
    if isinstance(right, list):
        if isinstance(left, pd.DatetimeIndex):
            return np.array([any(is_within(d, inter) for inter in right) for d in left])
        if isinstance(left, Interval):
            return any(is_within(left, inter) for inter in right)
        if isinstance(left, np.ndarray) and len(left) > 0 and isinstance(left[0], Interval):
            return np.array([any(is_within(inter_l, inter_r) for inter_r in right) for inter_l in left])

    # Case: Right is a vector of intervals (Recycling)
    if isinstance(right, np.ndarray) and len(right) > 0 and isinstance(right[0], Interval):
        if isinstance(left, pd.DatetimeIndex):
            res = []
            for i in range(len(left)):
                res.append(is_within(left[i], right[i % len(right)]))
            return np.array(res)
        if isinstance(left, Interval):
            return is_within(left, right[0]) # Simplified for single interval vs vector

    # Case: Basic single check
    if isinstance(right, Interval):
        if isinstance(left, pd.DatetimeIndex):
            return np.array([is_within(d, right) for d in left])
        return is_within(left, right)

    return False

# --- Script Execution ---
int_val = interval(ymd("2001-01-01"), ymd("2002-01-01"))
int2 = interval(ymd("2001-06-01"), ymd("2002-01-01"))

print(within(ymd("2001-05-03"), int_val)) 
print(within(int2, int_val)) 
print(within(ymd("1999-01-01"), int_val)) 

dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
blackout_vector = np.array([
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
])
# This expression is not printed in R source, but we evaluate it
_ = within(dates, blackout_vector)

dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
lst = [
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
]
print(within(dates, lst))

int_1 = interval(
    ymd("2014-12-20", "2014-12-30"),
    ymd("2015-01-01", "2015-01-03")
)
print(within(int_1, lst))