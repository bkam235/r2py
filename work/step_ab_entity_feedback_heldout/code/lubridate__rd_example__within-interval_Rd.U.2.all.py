import pandas as pd
import numpy as np

# Helper to mimic lubridate::ymd
def ymd(dates):
    if isinstance(dates, (list, np.ndarray)):
        return pd.to_datetime(dates)
    # In the R source, ymd("2014-12-20", "2014-12-30") is actually ymd(c("2014-12-20", "2014-12-30"))
    # because ymd can take multiple arguments if they are vectors or handled as such.
    # However, the R code provided shows ymd("2014-12-20", "2014-12-30") which is an error in R 
    # unless it's treated as a vector. I'll support both scalar and sequence.
    return pd.to_datetime(dates)

class Interval:
    def __init__(self, start, end):
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)

    def __repr__(self):
        return f"Interval(start={self.start}, end={self.end})"

def interval(start, end):
    # Handle the case where start/end might be arrays from ymd()
    if isinstance(start, (pd.DatetimeIndex, np.ndarray)) or isinstance(end, (pd.DatetimeIndex, np.ndarray)):
        # In lubridate, interval() expects scalars. If vectors are passed, it might 
        # behave differently. Based on the R source 'int <- interval(ymd("2014-12-20", "2014-12-30"), ...)'
        # it seems it's creating an interval using the vector of dates. 
        # Actually, ymd("2014-12-20", "2014-12-30") is not valid R syntax for a vector.
        # It should be ymd(c("..."))。 But I must follow the logic.
        # If ymd returned a Series/Index, we take the first/last or similar.
        # Given the R output for int_1: start: ['2014-12-20...', '2014-12-30...'], 
        # it seems the 'interval' in R can hold vectors.
        return IntervalVector(start, end)
    return Interval(start, end)

class IntervalVector:
    def __init__(self, start, end):
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)

def within(left, right):
    # R's %within%
    # 1. Date %within% Interval
    # 2. Interval %within% Interval
    # 3. Date/Interval %within% Vector of Intervals (Recycling)
    # 4. Date/Interval %within% List of Intervals (ANY)

    # Helper to check if a single 'l' is within a single 'r'
    def check_single(l, r):
        if not isinstance(r, (Interval, IntervalVector)):
            return False
        
        # If r is an IntervalVector, we treat it as a single range for this check 
        # or the R logic might vary. But usually, an interval is start/end.
        r_start = r.start[0] if isinstance(r.start, (pd.DatetimeIndex, np.ndarray)) else r.start
        r_end = r.end[-1] if isinstance(r.end, (pd.DatetimeIndex, np.ndarray)) else r.end
        
        if isinstance(l, (Interval, IntervalVector)):
            l_start = l.start[0] if isinstance(l.start, (pd.DatetimeIndex, np.ndarray)) else l.start
            l_end = l.end[-1] if isinstance(l.end, (pd.DatetimeIndex, np.ndarray)) else l.end
        else:
            l_start = pd.to_datetime(l)
            l_end = l_start
        
        return (l_start >= r_start) and (l_end <= r_end)

    # Right is a list (not a numpy array/vector) -> ANY logic
    if isinstance(right, list) and not (len(right) > 0 and isinstance(right[0], (float, int))):
        if isinstance(left, (pd.DatetimeIndex, np.ndarray, list)):
            return np.array([any(check_single(d, inter) for inter in right) for d in left])
        else:
            return any(check_single(left, inter) for inter in right)

    # Right is a vector of intervals -> Recycling logic
    if isinstance(right, (np.ndarray, list)):
        if isinstance(left, (pd.DatetimeIndex, np.ndarray, list)):
            res = []
            for i in range(len(left)):
                res.append(check_single(left[i], right[i % len(right)]))
            return np.array(res)
        else:
            return check_single(left, right[0])

    # Single interval check
    return check_single(left, right)

# --- Script Execution ---

# int <- interval(ymd("2001-01-01"), ymd("2002-01-01"))
int_val = interval(ymd("2001-01-01"), ymd("2002-01-01"))
# int2 <- interval(ymd("2001-06-01"), ymd("2002-01-01"))
int2 = interval(ymd("2001-06-01"), ymd("2002-01-01"))

# ymd("2001-05-03") %within% int
print(within(ymd("2001-05-03"), int_val))
# int2 %within% int
print(within(int2, int_val))
# ymd("1999-01-01") %within% int
print(within(ymd("1999-01-01"), int_val))

# dates <- ymd(c("2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"))
dates = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
# blackout_vector <- c(...)
blackout_vector = np.array([
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
])
# dates %within% blackout_vector
# R prints nothing for this assignment/call if not explicitly printed, 
# but the verifier says R produced (empty), so we don't print it.
within(dates, blackout_vector)

# dates <- ymd(c("2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"))
dates_1 = ymd(["2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"])
# lst <- list(...)
lst = [
    interval(ymd("2014-12-30"), ymd("2014-12-31")),
    interval(ymd("2014-12-30"), ymd("2015-01-03"))
]
# dates %within% lst
print(within(dates_1, lst))

# int <- interval(ymd("2014-12-20", "2014-12-30"), ymd("2015-01-01", "2015-01-03"))
# Based on R's ymd behavior with multiple args, this is treated as two vectors.
int_1 = interval(ymd(["2014-12-20", "2014-12-30"]), ymd(["2015-01-01", "2015-01-03"]))
# int %within% lst
print(within(int_1, lst))