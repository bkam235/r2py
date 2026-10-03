import pandas as pd
import numpy as np
import re

# r2py:entity:re_match
def re_match_impl(pattern, text, **kwargs):
    # Ensure text is a list of strings
    if isinstance(text, str):
        text = [text]
    
    # R's rematch uses perl=TRUE. Python's re is generally compatible.
    # R's (?<name>) is Python's (?P<name>)
    py_pattern = pattern.replace("(?<", "(?P<")
    regex = re.compile(py_pattern)
    
    results = []
    for t in text:
        match = regex.search(t)
        if match:
            # First column is the full match
            row = [match.group(0)]
            # Subsequent columns are capture groups
            row.extend(match.groups())
            results.append(row)
        else:
            # If no match, R produces a row of NAs
            # We need to know how many columns to produce
            num_groups = regex.groups
            results.append([None] * (1 + num_groups))
    
    # Determine column names
    col_names = [".match"]
    if regex.groupindex:
        # Use named groups if available
        col_names.extend(regex.groupindex.keys())
    else:
        # Use 1-based indexing for unnamed groups
        col_names.extend([str(i + 1) for i in range(regex.groups)])
    
    return pd.DataFrame(results, columns=col_names)

# r2py:entity:dates
dates = ["2016-04-20", "1977-08-08", "not a date", "2016",
  "76-03-02", "2012-06-30", "2015-01-21 19:58"]

# r2py:entity:isodate
isodate = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"

# r2py:entity:re_match
re_match = re_match_impl(isodate, dates)
print(re_match)

# r2py:entity:isodaten
isodaten = "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"

# r2py:entity:re_match_1
re_match_1 = re_match_impl(isodaten, dates)
print(re_match_1)