# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import re

# r2py:entity:re_match
def re_match(text, pattern, **kwargs):
    """
    Python implementation of the rematch2::re_match function.
    """
    if not isinstance(text, (list, tuple, pd.Series)):
        text = [text]
    
    texts = [str(t) for t in text]
    
    # R's rematch2 uses PCRE. Python's re handles (?P<name>...) 
    # but the input might be (?<name>...). We normalize for Python re.
    py_pattern = pattern.replace("(?<", "(?P<")
    regex = re.compile(py_pattern)
    
    results = []
    for t in texts:
        match = regex.search(t)
        if match:
            # Extract positional groups
            pos_groups = match.groups()
            
            # Create a dictionary for the row
            row = {}
            # The number of capture groups is regex.groups
            for i in range(1, regex.groups + 1):
                group_val = match.group(i)
                # Find name: check regex.groupindex (1-indexed in R, 1-indexed here)
                group_name = regex.groupindex.get(i) if False else None # regex.groupindex is {name: index}
                
                # We need to map index -> name
                # Find the name that corresponds to index i
                name_for_i = None
                for name, idx in regex.groupindex.items():
                    if idx == i:
                        name_for_i = name
                        break
                
                final_name = name_for_i if name_for_i else f"V{i}" if not regex.groupindex else f"group{i}"
                # R's rematch2 uses V1, V2... if no names are provided
                # But the verification output suggests 'group1' etc. for unnamed.
                # Wait, the R output showed empty column names for unnamed.
                # Actually, looking at the R output provided: 
                # <chr> <chr> <chr> .text .match
                # Those first 3 columns are the capture groups.
                
                row[final_name] = group_val
            
            row['.text'] = t
            row['.match'] = match.group(0)
        else:
            row = {'.text': t, '.match': None}
            
        results.append(row)
    
    df = pd.DataFrame(results)
    
    # The verification output suggests unnamed groups are simply columns.
    # Let's refine naming to match the R tibble (which often uses V1, V2 or empty).
    # If no names were provided in the regex, we'll use a generic approach.
    if not regex.groupindex:
        # Rename group1, group2... to empty or V1, V2. 
        # R tibbles usually name unnamed captures V1, V2... or leave them.
        # Based on the output: "  ``    ``    ``    .text    .match" 
        # It looks like they are unnamed. We'll use a placeholder.
        cols_to_rename = {f"group{i}": "" for i in range(1, regex.groups + 1)}
        df = df.rename(columns=cols_to_rename)

    # Ensure columns are ordered: Groups first, then .text, then .match
    cols = [c for c in df.columns if c not in ['.text', '.match']]
    cols = cols + ['.text', '.match']
    return df[cols]

# r2py:entity:dates
dates = ["2016-04-20", "1977-08-08", "not a date", "2016",
        "76-03-02", "2012-06-30", "2015-01-21 19:58"]
# r2py:entity:isodate
isodate = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"
# r2py:entity:re_match
print(re_match(text=dates, pattern=isodate))

# The same with named groups
# r2py:entity:isodaten
isodaten = "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"
# r2py:entity:re_match_1
print(re_match(text=dates, pattern=isodaten))