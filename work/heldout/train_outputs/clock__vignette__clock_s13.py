# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:x
x = ["2020/1/5", "10-03-05", "2020/2/2"]
# r2py:entity:formats
formats = ["%Y/%m/%d", "%y-%m-%d"]

# Python's pandas.to_datetime doesn't support a list of formats for a single vector 
# in the same way clock::date_parse does. We iterate through formats until parsed.
# r2py:entity:date_parse
def parse_dates(dates, formats):
    results = []
    for date_str in dates:
        parsed = np.nan
        for fmt in formats:
            try:
                parsed = pd.to_datetime(date_str, format=fmt)
                break
            except (ValueError, TypeError):
                continue
        results.append(parsed)
    return pd.to_datetime(results)

# r2py:entity:date_parse
date_parse = parse_dates(x, formats)
print(date_parse)