import re
import pandas as pd
import numpy as np

# r2py:entity:re_match
def re_match(pattern, text, **kwargs):
    if isinstance(text, (list, np.ndarray, pd.Series)):
        texts = [str(t) for t in text]
    else:
        texts = [str(text)]
    
    # R's re_match uses perl = TRUE, which allows named capture groups (?<name>...)
    # Python's re module uses (?P<name>...) for named groups.
    # We must transform the R-style named group syntax to Python-style for the engine.
    py_pattern = pattern.replace("(?<", "(?P<")
    compiled_re = re.compile(py_pattern)
    
    results = []
    group_names = list(compiled_re.groupindex.keys()) if compiled_re.groupindex else []
    
    for t in texts:
        match = compiled_re.search(t)
        if match:
            # .match is the full match (group 0)
            row = [match.group(0)]
            # Add capture groups in order
            for i in range(1, compiled_re.groups + 1):
                row.append(match.group(i))
        else:
            # Return NA (None) for match and all groups
            row = [None] * (1 + compiled_re.groups)
        results.append(row)
    
    # Column naming: .match followed by capture names (or V1, V2... if unnamed)
    cols = ['.match']
    if group_names:
        cols.extend(group_names)
    elif compiled_re.groups > 0:
        cols.extend([f'V{i}' for i in range(1, compiled_re.groups + 1)])
        
    return pd.DataFrame(results, columns=cols)

# r2py:entity:dates
dates = ["2016-04-20", "1977-08-08", "not a date", "2016",
  "76-03-02", "2012-06-30", "2015-01-21 19:58"]
# r2py:entity:isodate
isodate = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"
# r2py:entity:re_match
re_match_res1 = re_match(text=dates, pattern=isodate)
print(re_match_res1)

# The same with named groups
# r2py:entity:isodaten
isodaten = "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"
# r2py:entity:re_match_1
re_match_res2 = re_match(text=dates, pattern=isodaten)
print(re_match_res2)