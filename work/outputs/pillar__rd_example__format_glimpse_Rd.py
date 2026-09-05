# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/pillar__rd_example__format_glimpse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pillar__rd_example__format_glimpse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import reprlib

# r2py:entity:format_glimpse
def format_glimpse(x, inner=False):
    # Handle character/string types
    if isinstance(x, (str, np.ndarray)) and (isinstance(x, str) or (x.dtype.kind in 'SU')):
        # R's encodeString(quote="\"") wraps strings in double quotes
        if isinstance(x, str):
            return f'"{x}"'
        return np.array([f'"{val}"' for val in x])

    # Handle Factors (Categorical in pandas)
    if isinstance(x, pd.Categorical):
        # If any level contains a comma, quote them
        if any(',' in str(level) for level in x.categories):
            return np.array([f'"{val}"' for val in x])
        else:
            return np.array([str(val) for val in x])

    # Handle Lists
    if isinstance(x, list):
        if not inner and len(x) == 0:
            return "list()"
        
        res = []
        for item in x:
            # Recursive call
            formatted = format_glimpse(item, inner=True)
            
            # Logic to determine brackets:
            # R's format_glimpse.list logic:
            # - Lists use []
            # - Vectors (length > 1) use <>
            # - Scalars use no extra brackets
            
            if isinstance(item, list):
                res.append(f"[{formatted}]")
            elif isinstance(item, (np.ndarray, range)) or (isinstance(item, list) and len(item) > 1):
                # This part is tricky; if it's a simple sequence, wrap in <>
                # In the provided R logic: out[!scalar] <- paste0("<", out[!scalar], ">")
                # where scalar is true if length == 1
                val_str = " ".join(map(str, item)) if hasattr(item, '__iter__') else str(item)
                res.append(f"<{val_str}>")
            else:
                res.append(str(item))
        
        # Join the list elements by comma for a a "glimpse" look
        return ", ".join(res)

    # Handle numeric vectors/arrays (Default)
    if isinstance(x, (np.ndarray, range, list)):
        # For simple numeric vectors like 1:3
        return " ".join(map(str, x))
    
    return str(x)

# r2py:entity:writeLines
def write_lines(text):
    if isinstance(text, np.ndarray):
        for line in text:
            print(line)
    elif isinstance(text, list):
        for line in text:
            print(line)
    else:
        print(text)

# --- Translation of the script ---

# format_glimpse(1:3)
# r2py:entity:format_glimpse
print(format_glimpse(list(range(1, 4))))

# Lists use [], vectors inside lists use <>
# r2py:entity:format_glimpse_1
print(format_glimpse([list(range(1, 4))]))
# r2py:entity:format_glimpse_2
print(format_glimpse([1, list(range(2, 4))]))
# r2py:entity:format_glimpse_3
print(format_glimpse([[1], [list(range(2, 4))]]))
# r2py:entity:format_glimpse_4
print(format_glimpse([[1], [list(range(2, 4))]])) # R as.list(1) is just a list of 1
# r2py:entity:format_glimpse_5
print(format_glimpse([[]])) # character() is empty vector
# r2py:entity:format_glimpse_6
print(format_glimpse([None])) # NULL

# Character strings are always quoted
# r2py:entity:writeLines
write_lines(format_glimpse(np.array(list(letters[0:3]))))
# r2py:entity:writeLines_1
write_lines(format_glimpse(np.array(["A", "B, C"])))

# Factors are quoted only when needed
# Case 1: No commas in levels -> not quoted
# r2py:entity:writeLines_2
factor1 = pd.Categorical(list(letters[0:3]))
write_lines(format_glimpse(factor1))

# Case 2: Comma in levels -> quoted
# r2py:entity:writeLines_3
factor2 = pd.Categorical(["A", "B, C"])
write_lines(format_glimpse(factor2))