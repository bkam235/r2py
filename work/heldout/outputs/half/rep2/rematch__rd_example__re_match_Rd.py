# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import re

# r2py:entity:dates
dates = ["2016-04-20", "1977-08-08", "not a date", "2016",
         "76-03-02", "2012-06-30", "2015-01-21 19:58"]

# r2py:entity:isodate
isodate = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"

# r2py:entity:re_match
def re_match_impl(text, pattern):
    # R's re_match returns the full match + capture groups
    # To get the full match as the first column, we wrap the pattern in parentheses
    full_pattern = f"({pattern})"
    extracted = pd.Series(text).str.extract(full_pattern)
    
    # Rename the first column to .match
    cols = extracted.columns.tolist()
    cols[0] = ".match"
    extracted.columns = cols
    return extracted

re_match = re_match_impl(dates, isodate)
print(re_match)

# Note: R uses (?<name>...), Python uses (?P<name>...)
# r2py:entity:isodaten
isodaten = "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"
# Python's re module requires ?P for named groups, but we keep the variable value as per R source
# However, to make it work in Python extract, we must use ?P
py_isodaten = isodaten.replace("(?<", "(?P<")

# r2py:entity:re_match_1
re_match_1 = re_match_impl(dates, py_isodaten)
print(re_match_1)