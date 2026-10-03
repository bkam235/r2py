# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import re
import pandas as pd
import numpy as np

# r2py:entity:re_match
def re_match(pattern, text, **kwargs):
    if not isinstance(text, (list, np.ndarray, pd.Series)):
        text = [text]
    else:
        text = list(text)
    
    results = []
    
    # Compile pattern to check for named groups
    regex = re.compile(pattern)
    capture_names = list(regex.groupindex.keys()) if regex.groupindex else []
    
    for item in text:
        item_str = str(item)
        match = regex.search(item_str)
        if match:
            # The full match is always the first column (.match)
            row = [match.group(0)]
            # Add capture groups
            for i in range(1, regex.groups + 1):
                row.append(match.group(i))
        else:
            # No match: match and all groups are NA
            row = [None] * (1 + regex.groups)
        results.append(row)
    
    columns = ['.match']
    # R's capture.names attribute contains the names of the capture groups
    if capture_names:
        columns += capture_names
    else:
        # If there are unnamed groups, name them as strings of their index
        for i in range(1, regex.groups + 1):
            columns.append(str(i))
            
    return pd.DataFrame(results, columns=columns)

# r2py:entity:dates
dates = ["2016-04-20", "1977-08-08", "not a date", "2016",
  "76-03-02", "2012-06-30", "2015-01-21 19:58"]
# r2py:entity:isodate
isodate = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"
# r2py:entity:re_match
print(re_match(pattern=isodate, text=dates))

# The same with named groups
# r2py:entity:isodaten
isodaten = "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"
# To make it work with Python re, we must convert (?<name> to (?P<name> internally 
# but the variable isodaten itself should match the R source string.
# We handle the conversion inside the call or a wrapper.
# r2py:entity:re_match_1
def re_match_wrapper(pattern, text, **kwargs):
    # Convert R-style named groups (?<name>...) to Python-style (?P<name>...)
    python_pattern = re.sub(r'\(\?<([a-zA-Z0-9_]+)>', r'(?P<\1>', pattern)
    return re_match(**kwargs, pattern=python_pattern, text=text)

# r2py:entity:re_match_1
print(re_match_wrapper(pattern=isodaten, text=dates))