# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import re
import pandas as pd
import numpy as np

# r2py:entity:re_match
def re_match(pattern, text, **kwargs):
    if not isinstance(text, (list, np.ndarray, pd.Series)):
        text = [str(text)]
    else:
        text = [str(item) for item in text]
    
    # R's rematch uses perl=TRUE. Python's re is similar.
    # R uses (?<name>), Python uses (?P<name>).
    # We must convert R-style named groups to Python-style for the re engine.
    python_pattern = re.sub(r'\(\?<([a-zA-Z0-9_]+)>', r'(?P<\1>', pattern)
    compiled_re = re.compile(python_pattern)
    
    # Capture names from the original pattern to match R's output
    # R's attr(match, "capture.names") contains names of the groups
    group_names = list(compiled_re.groupindex.keys())
    
    results = []
    for item in text:
        match = compiled_re.search(item)
        if match:
            # .match is the full match
            row = [match.group(0)]
            # Captured groups
            row.extend(match.groups())
        else:
            # No match: .match and all groups are NA
            row = [None] * (1 + compiled_re.groups)
        results.append(row)
    
    # Column names: ".match" followed by capture names or indices
    cols = [".match"]
    if group_names:
        cols.extend(group_names)
    elif compiled_re.groups > 0:
        cols.extend([f"group{i+1}" for i in range(compiled_re.groups)])
        
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
re_match_res_n = re_match(text=dates, pattern=isodaten)
print(re_match_res_n)