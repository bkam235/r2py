# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd

# r2py:entity:pretty_ms
def parse_ms(ms):
    ms = np.array(ms)
    days = ms // (24 * 3600 * 1000)
    rem = ms % (24 * 3600 * 1000)
    hours = rem // (3600 * 1000)
    rem = rem % (3600 * 1000)
    minutes = rem // (60 * 1000)
    rem = rem % (60 * 1000)
    seconds = rem // 1000
    return np.column_stack([days, hours, minutes, seconds])

def first_positive(col):
    pos = np.where(col > 0)[0]
    return pos[0] if pos.size > 0 else None

def pretty_ms(ms, compact=False):
    ms = np.array(ms)
    if not np.issubdtype(ms.dtype, np.number):
        raise TypeError("ms must be numeric")
    
    parsed = parse_ms(ms)
    
    if compact:
        units = ["d", "h", "m", "s"]
        parsed2 = np.array([[f"{val}{unit}" if val > 0 else "" for val, unit in zip(row, units)] for row in parsed])
        
        results = []
        for i in range(len(ms)):
            row = parsed[i]
            idx = first_positive(row)
            if idx is not None:
                results.append(f"~{parsed2[i, idx]}")
            else:
                results.append(None)
        return np.array(results)
    else:
        exact = np.array([f"{int(np.ceil(val))}ms" if not np.isnan(val) else None for val in ms])
        
        def merge_pieces(pieces):
            if np.all(np.isnan(pieces)) or np.all(pieces == 0):
                return None
            parts = []
            labels = ["d", "h", "m", "s"]
            for val, label in zip(pieces, labels):
                if val > 0:
                    parts.append(f"{val}{label}")
            return " ".join(parts)

        approx = np.array([merge_pieces(row) for row in parsed])
        
        final = []
        for i in range(len(ms)):
            if np.isnan(ms[i]):
                final.append(None)
            elif ms[i] < 1000:
                final.append(exact[i])
            else:
                final.append(approx[i])
        return np.array(final)

# r2py:entity:pretty_ms
ms_vals = np.array([1337, 13370, 133700, 1337000, 1337000000])
print(pretty_ms(ms_vals))
# r2py:entity:pretty_ms_1
print(pretty_ms(ms_vals, compact=True))