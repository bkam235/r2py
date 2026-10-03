import re
import pandas as pd
import numpy as np

# r2py:entity:re_match
def re_match(pattern, text, **kwargs):
    if not isinstance(text, (list, np.ndarray, pd.Series)):
        text = [text]
    
    text_list = [str(t) for t in text]
    # R's perl=TRUE is equivalent to Python's re module
    regex = re.compile(pattern)
    
    matches = [regex.search(t) for t in text_list]
    
    # .match column (the full match)
    match_vals = [m.group(0) if m else None for m in matches]
    
    final_cols = [".match"]
    final_values = [match_vals]
    
    # R implementation: if ( !is.null(attr(match, "capture.start")) )
    # This means if the regex has capture groups.
    if regex.groups > 0:
        # R's capture.names is NULL if no groups are named.
        # If some are named, it provides names for all (unnamed ones get empty string or similar)
        # Actually, in R's regexpr(perl=TRUE), capture.names contains names of named groups
        # and empty strings for unnamed groups.
        
        capture_names = []
        for i in range(1, regex.groups + 1):
            # Find name of group i
            name = None
            for k, v in regex.groupindex.items():
                if v == i:
                    name = k
                    break
            capture_names.append(name if name else "")
            
        for i in range(1, regex.groups + 1):
            group_vals = [m.group(i) if m else None for m in matches]
            final_values.append(group_vals)
        
        # colnames(res) <- c(".match", attr(match, "capture.names"))
        # If capture_names is empty strings, R typically just labels them by index or leaves them.
        # But based on the R source, it uses the attribute directly.
        final_cols.extend(capture_names)

    # Construct DataFrame to simulate the matrix
    df = pd.DataFrame(np.array(final_values).T, columns=final_cols)
    return df.astype(object)

# r2py:entity:dates
dates = ["2016-04-20", "1977-08-08", "not a date", "2016",
  "76-03-02", "2012-06-30", "2015-01-21 19:58"]

# r2py:entity:isodate
isodate = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"

# First call: no named groups, so capture.names should be empty/null for the groups
# r2py:entity:re_match
print(re_match(pattern=isodate, text=dates))

# The same with named groups
# We store the R string as the variable value, but translate it for the function call
# r2py:entity:isodaten
isodaten = "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"

# Python requires ?P<name> instead of <name>
# r2py:entity:re_match_1
python_isodaten = isodaten.replace("(?<", "(?P<")
print(re_match(pattern=python_isodaten, text=dates))