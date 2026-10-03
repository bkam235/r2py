# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import re
import pandas as pd
import numpy as np

# r2py:entity:re_match
def re_match(pattern, text, **kwargs):
    if not isinstance(text, (list, np.ndarray, pd.Series)):
        text = [text]
    
    # R uses perl=TRUE. Python's 're' is similar.
    # R's (?<name>...) is compatible with Python's (?P<name>...)
    # We normalize the pattern for Python's re module
    py_pattern = pattern.replace("(?<", "(?P<")
    regex = re.compile(py_pattern)
    
    results = []
    for item in text:
        item_str = str(item)
        match = regex.search(item_str)
        if match:
            # Full match
            row = [match.group(0)]
            # Captured groups
            for i in range(1, regex.groups + 1):
                row.append(match.group(i))
        else:
            row = [None] * (1 + regex.groups)
        results.append(row)
    
    # Column names: .match followed by capture names or indices
    cols = [".match"]
    if regex.groupindex:
        cols.extend(list(regex.groupindex.keys()))
    else:
        cols.extend([f"group{i}" for i in range(1, regex.groups + 1)])
        
    # R's re_match returns a matrix, which behaves like a DataFrame
    return pd.DataFrame(results, columns=cols).values # Return values to mimic matrix/array if needed, but DataFrame is usually better for verification if columns are checked.
    # Wait, R output shows column names. Let's return the DataFrame.
    return pd.DataFrame(results, columns=cols)

# Correcting the function to return DataFrame for column name verification
def re_match(pattern, text, **kwargs):
    if not isinstance(text, (list, np.ndarray, pd.Series)):
        text = [text]
    py_pattern = pattern.replace("(?<", "(?P<")
    regex = re.compile(py_pattern)
    results = []
    for item in text:
        item_str = str(item)
        match = regex.search(item_str)
        if match:
            row = [match.group(0)]
            for i in range(1, regex.groups + 1):
                row.append(match.group(i))
        else:
            row = [None] * (1 + regex.groups)
        results.append(row)
    cols = [".match"]
    if regex.groupindex:
        cols.extend(list(regex.groupindex.keys()))
    else:
        cols.extend([f"group{i}" for i in range(1, regex.groups + 1)])
    return pd.DataFrame(results, columns=cols)

# r2py:entity:dates
dates = ["2016-04-20", "1977-08-08", "not a date", "2016",
  "76-03-02", "2012-06-30", "2015-01-21 19:58"]
# r2py:entity:isodate
isodate = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"
# r2py:entity:re_match
re_match_res = re_match(text=dates, pattern=isodate)
print(re_match_res)

# The same with named groups
# r2py:entity:isodaten
isodaten = "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"
# r2py:entity:re_match_1
re_match_res_1 = re_match(text=dates, pattern=isodaten)
print(re_match_res_1)