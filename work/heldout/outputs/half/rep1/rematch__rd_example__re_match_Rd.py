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
    
    # R's rematch uses (?<name>...) for named groups, 
    # Python uses (?P<name>...). We convert for the re engine.
    py_pattern = pattern.replace("(?<", "(?P<")
    
    regex = re.compile(py_pattern)
    capture_names = list(regex.groupindex.keys())
    
    results = []
    for item in text:
        item_str = str(item)
        match = regex.search(item_str)
        if match:
            # .match is the full match
            row = [match.group(0)]
            # Append capture groups
            row.extend(match.groups())
            results.append(row)
        else:
            # No match: full match and all groups are NA
            row = [None] * (1 + regex.groups)
            results.append(row)
            
    columns = ['.match'] + capture_names
    # If there were groups but no names, name them 1, 2, 3...
    if len(columns) < (len(results[0]) if results else 0):
        needed = (len(results[0]) if results else 0) - len(columns)
        columns += [str(i+1) for i in range(needed)]
    
    df = pd.DataFrame(results, columns=columns)
    return df

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
# r2py:entity:re_match_1
print(re_match(pattern=isodaten, text=dates))