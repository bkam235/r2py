# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 10

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:entity:x
def year_month_day(year, month=None, day=None):
    if isinstance(day, (range, np.ndarray, list)):
        return [datetime(year, month, d) for d in day]
    return datetime(year, month, day)

def as_naive_time(x):
    if not isinstance(x, list):
        return [x]
    return x

# r2py:entity:as_weekday
def as_weekday(x):
    # R clock: Sunday=1, Monday=2, ..., Saturday=7
    # Python isoweekday: Monday=1, ..., Sunday=7
    def map_weekday(dt):
        iso = dt.isoweekday()
        return iso + 1 if iso < 7 else 1
    
    res = [map_weekday(dt) for dt in x]
    # Format for printing to match R output style: <weekday[n]> [Tue Wed]
    return res

# r2py:entity:monday
def weekday(code):
    return int(code)

class ClockWeekdays:
    monday = 2
    tuesday = 3
    wednesday = 4
    thursday = 5
    friday = 6
    saturday = 7
    sunday = 1

clock_weekdays = ClockWeekdays()

# r2py:entity:time_point_shift
def time_point_shift(x, target, which="next", boundary="keep"):
    res = []
    for dt in x:
        # Current weekday: Sun=1, Mon=2, ...
        current_wd = (dt.isoweekday() + 1) if dt.isoweekday() < 7 else 1
        
        work_dt = dt
        if which == "next":
            if boundary == "advance":
                work_dt = work_dt + timedelta(days=1)
            
            # Recalculate current_wd if advanced
            curr = (work_dt.isoweekday() + 1) if work_dt.isoweekday() < 7 else 1
            diff = target - curr
            if diff < 0:
                diff += 7
            work_dt = work_dt + timedelta(days=diff)
            
        elif which == "previous":
            if boundary == "advance":
                work_dt = work_dt - timedelta(days=1)
            
            curr = (work_dt.isoweekday() + 1) if work_dt.isoweekday() < 7 else 1
            diff = curr - target
            if diff < 0:
                diff += 7
            work_dt = work_dt - timedelta(days=diff)
            
        res.append(work_dt)
    return res

def format_clock_output(val, type_name):
    if isinstance(val, list):
        if type_name == "weekday":
            # Map numeric back to names for printing
            mapping = {1: "Sun", 2: "Mon", 3: "Tue", 4: "Wed", 5: "Thu", 6: "Fri", 7: "Sat"}
            names = " ".join([mapping[v] for v in val])
            return f"      <weekday[{len(val)}]> \n[1] {names}"
        elif type_name == "naive_time":
            dates = " ".join([f'"{d.strftime("%Y-%m-%d")}"' for d in val])
            return f"      <naive_time<day>[{len(val)}]> \n[1] {dates}"
    return str(val)

# --- Main Script ---

# r2py:entity:x
x = as_naive_time(year_month_day(2019, 1, range(1, 3)))

# A Tuesday and Wednesday
# r2py:entity:as_weekday
print(format_clock_output(as_weekday(x), "weekday"))

# r2py:entity:monday
monday = weekday(clock_weekdays.monday)

# Shift to the next Monday
# r2py:entity:time_point_shift
print(format_clock_output(time_point_shift(x, monday), "naive_time"))

# Shift to the previous Monday
# r2py:entity:time_point_shift_1
print(format_clock_output(time_point_shift(x, monday, which="previous"), "naive_time"))

# What about Tuesday?
# r2py:entity:tuesday
tuesday = weekday(clock_weekdays.tuesday)

# Notice that the day that was currently on a Tuesday was not shifted
# r2py:entity:time_point_shift_2
print(format_clock_output(time_point_shift(x, tuesday), "naive_time"))

# You can force it to "advance"
# r2py:entity:time_point_shift_3
print(format_clock_output(time_point_shift(x, tuesday, boundary="advance"), "naive_time"))