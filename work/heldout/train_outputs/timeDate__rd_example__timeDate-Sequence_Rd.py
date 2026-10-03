import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from dateutil import parser

# r2py:entity:t1
def which_format(charvec):
    if not charvec or pd.isna(charvec):
        return "unknown"
    c1 = str(charvec)
    nchar = len(c1)
    substr = (nchar >= 5 and c1[4] == "-")
    
    if "/" in c1 and len(c1.split("/")) == 3:
        return "%m/%d/%Y"
    if "-" in c1 and any(len(part) == 3 for part in c1.split("-")):
        return "%d-%b-%Y"
    if nchar == 4 and not substr:
        return "%Y"
    if nchar == 7 and substr:
        return "%Y-%m"
    if nchar == 10 and substr:
        return "%Y-%m-%d"
    if nchar == 13 and substr:
        return "%Y-%m-%d %H"
    if nchar == 16 and substr:
        return "%Y-%m-%d %H:%M"
    if nchar == 19 and substr:
        return "%Y-%m-%d %H:%M:%S"
    if nchar >= 20 and substr and c1[19] == ".":
        return "%Y-%m-%d %H:%M:%S"
    if nchar == 6 and not substr:
        return "%Y%m"
    if nchar == 8 and not substr:
        return "%Y%m%d"
    if nchar == 10 and not substr:
        return "%Y%m%d%H"
    if nchar == 12 and not substr:
        return "%Y%m%d%H%M"
    if nchar == 14 and not substr:
        return "%Y%m%d%H%M%S"
    return "unknown"

def time_date(charvec, format_val=None, zone="GMT", fin_center="GMT"):
    tz = pytz.timezone(zone)
    if format_val:
        try:
            dt = datetime.strptime(charvec, format_val)
        except ValueError:
            dt = parser.parse(charvec)
    else:
        dt = parser.parse(charvec)
    
    try:
        return tz.localize(dt, is_dst=None)
    except pytz.NonExistentTimeError:
        return None 
    except pytz.AmbiguousTimeError:
        return tz.localize(dt, is_dst=False)

def time_sequence(from_val, to_val=None, by="day", length_out=None, format_val=None, zone="GMT", fin_center="GMT"):
    if zone == "": zone = "GMT"
    if fin_center == "": fin_center = "GMT"
    
    if to_val is None:
        to_val = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    if format_val is None:
        fmt_from = which_format(str(from_val))
        fmt_to = which_format(str(to_val))
    else:
        fmt_from = fmt_to = format_val
        
    start_dt = time_date(str(from_val), format_val=fmt_from, zone=zone, fin_center=fin_center)
    if start_dt is None:
        raise ValueError(f"argument 'from' specifies a non-existent time in time zone '{fin_center}'")
        
    end_dt = time_date(str(to_val), format_val=fmt_to, zone=zone, fin_center=fin_center)
    
    if by == "DSTday":
        # Wall-clock time preservation
        dates = pd.date_range(start=start_dt, end=end_dt, freq='D', tz=zone)
    elif by == "day":
        # 24-hour increments (POSIXct behavior)
        dates = []
        curr = start_dt
        while curr <= end_dt:
            dates.append(curr)
            curr += timedelta(days=1)
        dates = pd.DatetimeIndex(dates)
    else:
        dates = pd.date_range(start=start_dt, end=end_dt, freq='S', tz=zone)

    if length_out is not None:
        dates = dates[:length_out]
        
    return dates

def print_r_style(dates, zone):
    print(f"     {zone}")
    formatted = []
    for d in dates:
        if d.hour == 0 and d.minute == 0 and d.second == 0:
            formatted.append(f"[{d.strftime('%Y-%m-%d')}]")
        else:
            formatted.append(f"[{d.strftime('%Y-%m-%d %H:%M:%S')}]")
    
    for i in range(0, len(formatted), 5):
        chunk = formatted[i:i+5]
        idx = i + 1
        print(f"[{idx}] " + " ".join(chunk))

# --- Execution ---

# autodetection of format
t1 = time_sequence(from_val="2004-03-12", to_val="2004-04-11")
print_r_style(t1, "GMT")

# stopifnot simulations
# r2py:entity:stopifnot
assert np.array_equal(t1, time_sequence(from_val="2004-03-12", to_val="11-Apr-2004"))
assert np.array_equal(t1, time_sequence(from_val="2004-03-12", to_val="2004-04-11", 
                                        format_val="%Y-%m-%d", fin_center="GMT"))

# observe "switch to summer time":
# r2py:entity:timeSequence
res_ts = time_sequence(from_val="2004-03-26 05:00:00", to_val="2004-04-02 05:00:00", 
                    zone="Europe/Zurich", fin_center="Europe/Zurich")
print_r_style(res_ts, "Europe/Zurich")

# ensure fixed clock time:
# r2py:entity:timeSequence_1
res_ts1 = time_sequence(from_val="2004-03-26 05:00:00", to_val="2004-04-01 05:00:00", 
                    by="DSTday", zone="Europe/Zurich", fin_center="Europe/Zurich")
print_r_style(res_ts1, "Europe/Zurich")

# on the day of DST change the time may not exist (notice 2004-03-28 00:00:00):
# r2py:entity:timeSequence_2
res_ts2 = time_sequence(from_val="2004-03-26 01:00:00", to_val="2004-04-01 01:00:00", 
                    by="DSTday", zone="Europe/Zurich", fin_center="Europe/Zurich")
print_r_style(res_ts2, "Europe/Zurich")