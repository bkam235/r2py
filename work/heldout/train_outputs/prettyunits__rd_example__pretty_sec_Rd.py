# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd
import math

# r2py:entity:pretty_sec
def parse_ms(ms):
    """Helper to simulate parse_ms logic (splitting ms into days, hours, mins, secs)"""
    ms = np.atleast_1d(ms)
    days = ms // (1000 * 60 * 60 * 24)
    rem = ms % (1000 * 60 * 60 * 24)
    hours = rem // (1000 * 60 * 60)
    rem = rem % (1000 * 60 * 60)
    mins = rem // (1000 * 60)
    secs = (rem % (1000 * 60)) // 1000
    return np.column_stack([days, hours, mins, secs])

def first_positive(x):
    """Helper to find index of first non-zero element"""
    for i, val in enumerate(x):
        if val > 0:
            return i
    return None

def pretty_ms(ms, compact=False):
    ms = np.atleast_1d(ms)
    parsed = parse_ms(ms)
    
    if compact:
        units = ["d", "h", "m", "s"]
        results = []
        for i in range(len(ms)):
            row = parsed[i]
            idx = first_positive(row)
            if idx is not None:
                results.append(f"~{int(row[idx])}{units[idx]}")
            else:
                results.append(None)
        return np.array(results)
    else:
        results = []
        for i in range(len(ms)):
            val_ms = ms[i]
            if pd.isna(val_ms):
                results.append(None)
                continue
            
            if val_ms < 1000:
                results.append(f"{math.ceil(val_ms)}ms")
            else:
                row = parsed[i].astype(int)
                pieces = []
                if row[0] > 0: pieces.append(f"{row[0]}d ")
                if row[1] > 0: pieces.append(f"{row[1]}h ")
                if row[2] > 0: pieces.append(f"{row[2]}m ")
                if row[3] > 0: pieces.append(f"{row[3]}s ")
                
                res_str = "".join(pieces).strip()
                results.append(res_str if res_str else None)
        return np.array(results)

def pretty_sec(sec, compact=False):
    return pretty_ms(np.atleast_1d(sec) * 1000, compact=compact)

# Execution
# r2py:entity:pretty_sec
print(pretty_sec(np.array([1337, 13370, 133700, 1337000, 13370000])))
# r2py:entity:pretty_sec_1
print(pretty_sec(np.array([1337, 13370, 133700, 1337000, 13370000]), compact=True))