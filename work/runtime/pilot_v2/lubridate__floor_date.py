import numpy as np
import pandas as pd
from pandas import Timestamp
from datetime import timedelta
import calendar

def r_floor_date(x, unit="seconds", week_start=7, *args, **kwargs):
    """
    Reproduces lubridate::floor_date in Python.
    """
    # Handle empty input
    if x is None:
        return None
    if isinstance(x, (list, np.ndarray, pd.Series)) and len(x) == 0:
        return x

    # Convert input to pandas Series for uniform processing
    # Note: x arrives as numpy array or scalar.
    if isinstance(x, np.ndarray):
        s = pd.Series(x)
    elif isinstance(x, list):
        s = pd.Series(x)
    elif isinstance(x, pd.Series):
        s = x
    else:
        s = pd.Series([x])

    # Convert to datetime objects. R's POSIXct is usually treated as Timestamps.
    # pd.to_datetime handles NaT correctly.
    s = pd.to_datetime(s)

    # If unit is a date/datetime (POSIXct/Date in R)
    if isinstance(unit, (Timestamp, np.datetime64, pd.Timestamp)):
        target = pd.to_datetime(unit)
        def floor_to_posix(t, u):
            if pd.isna(t): return pd.NaT
            return t if t < u else u
        results = s.apply(lambda t: floor_to_posix(t, target))
    else:
        unit_str = str(unit)

        def floor_single(t):
            if pd.isna(t):
                return pd.NaT
            
            # R's floor_date mapping
            if unit_str == "seconds":
                return t.floor('S')
            elif unit_str == "minutes":
                return t.floor('T')
            elif unit_str == "hours":
                return t.floor('H')
            elif unit_str == "days" or unit_str == "day":
                return t.floor('D')
            elif unit_str == "weeks" or unit_str == "week":
                # R's week_start: 7 is Sunday, 1 is Monday.
                # t.weekday() is 0=Mon, 6=Sun.
                weekday_r = t.weekday() + 1 
                diff = (weekday_r - week_start) % 7
                res = t - pd.Timedelta(days=diff)
                return res.replace(hour=0, minute=0, second=0, microsecond=0)
            elif unit_str == "months" or unit_str == "month":
                return t.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif unit_str == "quarters" or unit_str == "quarter":
                month = t.month
                quarter_start_month = ((month - 1) // 3) * 3 + 1
                return t.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
            elif unit_str == "years" or unit_str == "year":
                return t.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                try:
                    return t.floor(unit_str)
                except:
                    return t

        results = s.apply(floor_single)

    # The harness fails because we returned .values (numpy array of nanoseconds integers)
    # instead of the Timestamp objects. R's POSIXct should be represented as 
    # Timestamp/datetime objects in Python.
    
    if isinstance(x, np.ndarray):
        # Convert Series of Timestamps to a numpy array of objects (Timestamps/NaT)
        return results.to_list() if results.dtype == 'datetime64[ns]' else results.values.astype(object)
    
    # Based on the fail logs, R returns lists of strings/dates. 
    # Returning the list of Timestamps is the natural Python equivalent.
    if isinstance(x, list):
        return results.tolist()
    
    if isinstance(x, pd.Series):
        return results

    # Scalar case
    val = results.iloc[0]
    if pd.isna(val):
        return np.nan
    return val

# Correcting the array return: a numpy array of timestamps should be dtype='object' 
# to avoid being cast to nanoseconds integers (which the harness saw as 1791273709000000000).
def r_floor_date(x, unit="seconds", week_start=7, *args, **kwargs):
    if x is None: return None
    
    # Handle scalar vs vector
    is_scalar = not isinstance(x, (list, np.ndarray, pd.Series))
    
    if is_scalar:
        working_list = [x]
    elif isinstance(x, pd.Series):
        working_list = x.tolist()
    else:
        working_list = list(x)
        
    if len(working_list) == 0:
        return x

    # Process using pandas for date logic
    s = pd.to_datetime(pd.Series(working_list))
    
    if isinstance(unit, (Timestamp, np.datetime64, pd.Timestamp)):
        target = pd.to_datetime(unit)
        results = s.apply(lambda t: target if t >= target else t if pd.notna(t) else pd.NaT)
    else:
        unit_str = str(unit)
        def floor_single(t):
            if pd.isna(t): return pd.NaT
            if unit_str == "seconds": return t.floor('S')
            if unit_str == "minutes": return t.floor('T')
            if unit_str == "hours": return t.floor('H')
            if unit_str in ["days", "day"]: return t.floor('D')
            if unit_str in ["weeks", "week"]:
                weekday_r = t.weekday() + 1 
                diff = (weekday_r - week_start) % 7
                return (t - pd.Timedelta(days=diff)).replace(hour=0, minute=0, second=0, microsecond=0)
            if unit_str in ["months", "month"]: return t.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if unit_str in ["quarters", "quarter"]:
                qs_month = ((t.month - 1) // 3) * 3 + 1
                return t.replace(month=qs_month, day=1, hour=0, minute=0, second=0, microsecond=0)
            if unit_str in ["years", "year"]: return t.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            return t.floor(unit_str) if hasattr(t, 'floor') else t

        results = s.apply(floor_single)

    # Convert back to natural Python objects
    final_list = [val if pd.notna(val) else None for val in results]
    
    if is_scalar:
        return final_list[0]
    if isinstance(x, np.ndarray):
        return np.array(final_list, dtype=object)
    if isinstance(x, pd.Series):
        return pd.Series(final_list)
    return final_list
