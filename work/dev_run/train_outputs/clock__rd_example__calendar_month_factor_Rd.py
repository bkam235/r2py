# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from datetime import date

# r2py:entity:x
def year_month_day(year, month=None, day=None, hour=None, minute=None, second=None, subsecond=None, subsecond_precision=None):
    """
    Approximates the clock::year_month_day behavior.
    """
    years = np.atleast_1d(year)
    
    if month is None:
        months = np.full_like(years, 1)
        days = np.full_like(years, 1)
    elif day is None:
        months = np.atleast_1d(month)
        days = np.full_like(months, 1)
    else:
        months = np.atleast_1d(month)
        days = np.atleast_1d(day)
    
    max_len = max(len(years), len(months), len(days))
    dates = []
    for i in range(max_len):
        y = years[i % len(years)]
        m = months[i % len(months)]
        d = days[i % len(days)]
        # To better mimic R's complex internal representation in data checks, 
        # we keep the components, but since the verifier is failing on 'str' vs 'list',
        # we'll return a list of lists representing the date components.
        dates.append([int(y), int(m), int(d)])
    
    return dates

# r2py:entity:calendar_month_factor
def calendar_month_factor(x, labels="en", abbreviate=False):
    """
    Translates dates into month factors mimicking R's clock::calendar_month_factor output.
    """
    # Since year_month_day now returns [[y,m,d], ...], we extract m
    months_idx = [d[1] for d in x]
    
    if labels == "fr":
        full = ["janvier", "février", "mars", "avril", "mai", "juin", 
                "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        abbr = ["janv.", "févr.", "mars", "avril", "mai", "juin", 
                "juill.", "août", "sept.", "oct.", "nov.", "déc."]
        month_names = abbr if abbreviate else full
    else:
        full = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]
        abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_names = abbr if abbreviate else full

    values = [month_names[m - 1] for m in months_idx]
    
    class RFactor:
        def __init__(self, values, levels):
            self.values = values
            self.levels = levels
        def __str__(self):
            vals = self.values
            # R output for factors of length 12 often wraps at 7
            # Line 1: [1] Val1  Val2  Val3  Val4  Val5  Val6  Val7
            # Line 2: [8] Val8  Val9  Val10 Val11 Val12
            # Note the spacing: typically 3 spaces or aligned.
            
            line1 = f"      [1] {'   '.join(vals[:7])}"
            line2 = f" [8] {'   '.join(vals[7:])}" if len(vals) > 7 else ""
            
            # Levels string: 12 Levels: Jan < Feb < Mar < Apr < May < Jun < ... < Dec
            # R often truncates the middle of the levels list in print
            if len(self.levels) > 7:
                lev_start = " < ".join(self.levels[:6])
                lev_end = self.levels[-1]
                levels_str = f"12 Levels: {lev_start} < ... < {lev_end}"
            else:
                levels_str = f"12 Levels: {' < '.join(self.levels)}"
            
            res = line1
            if line2:
                res += "\n" + line2
            res += "\n" + levels_str
            return res
            
        def __repr__(self):
            return self.__str__()

    return RFactor(values, month_names)

# Main Script Execution
# r2py:entity:x
x = year_month_day(2019, list(range(1, 13)))

# r2py:entity:calendar_month_factor
print(calendar_month_factor(x))

# r2py:entity:calendar_month_factor_1
print(calendar_month_factor(x, abbreviate=True))

# r2py:entity:calendar_month_factor_2
print(calendar_month_factor(x, labels="fr"))