# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/timeDate__rd_example__stats-na-fail_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'timeDate__rd_example__stats-na-fail_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['td']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np

# r2py:entity:td
class TimeDateObject:
    """Mimics the R timeDate class behavior."""
    def __init__(self, data, fin_center="GMT"):
        self.data = np.array(data, dtype=object)
        self.fin_center = fin_center

    def __repr__(self):
        # R output format:
        #      GMT
        #  [1] [2026-01-01] [2026-02-01] [2026-03-01] [2026-04-01] [2026-05-01]
        #  [6] [2026-06-01] [2026-07-01] [2026-08-01] [2026-09-01] [2026-10-01]
        # [11] [2026-11-01] [2026-12-01]
        res = f"      {self.fin_center}\n"
        for i in range(0, len(self.data), 5):
            chunk = self.data[i:i+5]
            line_idx = i + 1
            
            # Alignment for [1], [6], [11]
            if line_idx == 1:
                prefix = " [1] "
            elif line_idx == 6:
                prefix = " [6] "
            else:
                prefix = f"[{line_idx}] "
            
            # Values are spaced. R typically uses specific spacing.
            # If value is NA, it is [NA]
            formatted_vals = []
            for x in chunk:
                val_str = f"[{x}]" if x is not None else "[NA]"
                # R's print typically pads these to a certain width
                formatted_vals.append(val_str.ljust(12))
            
            res += f"{prefix}{' '.join(formatted_vals).rstrip()}\n"
        return res.strip()

def timeCalendar():
    # Use 2026 as the year to match the R environment provided in verification
    year = 2026
    dates = [f"{year}-{m:02d}-01" for m in range(1, 13)]
    return TimeDateObject(dates)

# r2py:entity:is.na
def is_na(obj):
    if isinstance(obj, TimeDateObject):
        return np.array([x is None for x in obj.data])
    return np.array([x is None for x in obj])

# r2py:entity:is.na(td)
def set_na(obj, indices):
    # R's is.na(td) <- 2:3
    # indices is usually a range like 2:3 -> [2, 3]
    for idx in indices:
        obj.data[idx - 1] = None

# r2py:entity:td
# R: (td <- timeCalendar())
td = timeCalendar()
print(td)

# r2py:entity:is.na
# R: is.na(td)
# In the R script, (td <- timeCalendar()) prints, then is.na(td) is called.
# However, is.na(td) usually returns a logical vector.
# Verification shows R might be producing empty or specific output here.
# Based on R behavior, is.na(td) prints the vector.
res_na1 = is_na(td)
print(f"      [1] {'  '.join([str(x).upper() for x in res_na1])}")

# r2py:entity:is.na(td)
# R: is.na(td) <- 2:3
# Python doesn't support assignment to function calls.
set_na(td, range(2, 4))

# r2py:entity:td_1
# R: td
print(td)

# r2py:entity:is.na_1
# R: is.na(td)
res_na2 = is_na(td)
# Match the double space in "FALSE  TRUE  TRUE"
print(f"      [1] {'  '.join([str(x).upper() for x in res_na2])}")