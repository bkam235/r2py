import pandas as pd
import numpy as np
from datetime import datetime

def ymd(*args):
    # In R, ymd("2001-01-01", "2001-01-02") returns a vector of dates
    # If a list/array is passed as the first arg, we handle that.
    if len(args) == 1 and isinstance(args[0], (list, np.ndarray)):
        return pd.to_datetime(args[0])
    if len(args) == 1:
        return pd.to_datetime(args[0])
    # Handle multiple positional arguments as a vector
    return pd.to_datetime(list(args))

class LubridateInterval:
    def __init__(self, start, end):
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        # R intervals often store the duration (.Data)
        self.data = (self.end - self.start).total_seconds()

    def __repr__(self):
        return f"Interval(start={self.start}, end={self.end})"

def interval(start, end):
    # Handle potential vectors in start/end
    if isinstance(start, (pd.DatetimeIndex, list, np.ndarray)) or \
       isinstance(end, (pd.DatetimeIndex, list, np.ndarray)):
        # Return a list of intervals for vectorization
        starts = pd.to_datetime(start) if not isinstance(start, (pd.DatetimeIndex, list, np.ndarray)) else start
        ends = pd.to_datetime(end) if not isinstance(end, (pd.DatetimeIndex, list, np.ndarray)) else end
        
        # Ensure both are the same length if they are vectors
        if hasattr(starts, '__len__') and hasattr(ends, '__len__'):
            return [LubridateInterval(s, e) for s, e in zip(starts, ends)]
        elif hasattr(starts, '__len__'):
            return [LubridateInterval(s, ends) for s in starts]
        elif hasattr(ends, '__len__'):
            return [LubridateInterval(starts, e) for e in ends]
    
    return LubridateInterval(start, end)

def within(left, right):
    # Helper to check if a single date is within a single interval
    def is_within(date, inter):
        d = pd.to_datetime(date)
        return (d >= inter.start) and (d <= inter.end)
    
    # Helper to check if a single interval is within a single interval
    def is_inter_within(inner, outer):
        return (inner.start >= outer.start) and (inner.end <= outer.end)

    # Right is a list of intervals
    if isinstance(right, list):
        # Left is a vector of dates
        if isinstance(left, (pd.DatetimeIndex, list, np.ndarray)):
            # If 'right' is a list, R's %within% treats it as "within ANY of these"
            res = []
            for d in left:
                res.append(any(is_within(d, inter) for inter in right))
            return np.array(res)
        # Left is a single date
        elif not isinstance(left, LubridateInterval):
            return any(is_within(left, inter) for inter in right)
        # Left is a single interval
        elif isinstance(left, LubridateInterval):
            return any(is_inter_within(left, inter) for inter in right)

    # Right is a single interval
    if isinstance(right, LubridateInterval):
        # Left is a vector of dates
        if isinstance(left, (pd.DatetimeIndex, list, np.ndarray)):
            res = []
            for d in left:
                res.append(is_within(d, right))
            return np.array(res)
        # Left is a single interval
        if isinstance(left, LubridateInterval):
            return is_inter_within(left, right)
        # Left is a single date
        return is_within(left, right)
    
    # Right is a vector of intervals (not a list, but a numpy array or similar)
    if isinstance(right, np.ndarray):
        if isinstance(left, (pd.DatetimeIndex, list, np.ndarray)):
            res = []
            for i in range(len(left)):
                res.append(is_within(left[i], right[i % len(right)]))
            return np.array(res)

    return False

# --- Script execution ---

int_val = interval(ymd("2001-01-01"), ymd("2002-01-01"))
int = int_val # Rename to int to match R
int2 = interval(ymd("2001-06-01"), ymd("2002-01-01"))

print(within(ymd("2001-05-03"), int)) 
print(within(int2, int)) 
print(within(ymd("1999-01-01"), int)) 

dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
blackout_vector = np.array([
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
])
# Note: In R, dates %within% blackout_vector uses recycling
# The result for this specific case is [FALSE, TRUE, FALSE, TRUE]
print(within(dates, blackout_vector))

dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
lst = [
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
]
print(within(dates, lst))

# int <- interval(ymd("2014-12-20", "2014-12-30"), ymd("2015-01-01", "2015-01-03"))
# In R, ymd("2014-12-20", "2014-12-30") returns a vector of 2 dates.
# The interval() function then creates a vector of 2 intervals.
int = interval(
    ymd("2014-12-20", "2014-12-30"),
    ymd("2015-01-01", "2015-01-03")
)
# R: int %within% lst 
# Since int is a vector of intervals and lst is a list, R checks if each 
# interval in 'int' is within ANY interval in 'lst'.
if isinstance(int, list):
    res = []
    for i_val in int:
        res.append(any(is_inter_within(i_val, outer) for outer in lst))
    print(np.array(res))
else:
    print(within(int, lst))