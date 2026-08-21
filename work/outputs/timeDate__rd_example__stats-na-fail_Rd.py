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
from datetime import datetime

# r2py:entity:td
class TimeDateObject:
    """Mimics the R timeDate class behavior."""
    def __init__(self, data, fin_center="GMT"):
        self.data = np.array(data, dtype=object)
        self.fin_center = fin_center

    def __repr__(self):
        # Mimics R's print output for timeCalendar:
        #      GMT
        #  [1] [2026-01-01] [2026-02-01] [2026-03-01] [2026-04-01] [2026-05-01]
        #  [6] [2026-06-01] [2026-07-01] [2026-08-01] [2026-09-01] [2026-10-01]
        # [11] [2026-11-01] [2026-12-01]
        res = f"      {self.fin_center}\n"
        for i in range(0, len(self.data), 5):
            chunk = self.data[i:i+5]
            # Format: [index] [val1] [val2] ...
            # Indices: [1], [6], [11]
            line_idx = i + 1
            prefix = f" [{line_idx}] " if line_idx > 1 else f" [1] "
            if line_idx >= 10:
                prefix = f"[{line_idx}] "
            
            formatted_vals = " ".join([f"[{str(x) if x is not None else 'NA'}]" for x in chunk])
            res += f"{prefix}{formatted_vals}\n"
        return res.strip()

# r2py:entity:is.na
    def is_na(self):
        return np.array([x is None for x in self.data])

# r2py:entity:is.na(td)
    def set_na(self, indices):
        for idx in indices:
            # R indices are 1-based
            self.data[idx - 1] = None

def timeCalendar():
    # Default: current year (mocked to 2026 based on R output), months 1:12, day 1
    year = 2026
    dates = [f"{year}-{m:02d}-01" for m in range(1, 13)]
    return TimeDateObject(dates)

# R: (td <- timeCalendar())
td = timeCalendar()
print(td)

# R: is.na(td)
# r2py:entity:is.na
is_na_td = td.is_na()
# R's is.na prints as: [1] FALSE FALSE ...
vals_na = "  ".join([str(x).upper() for x in is_na_td])
print(f"      [1] {vals_na}")

# R: is.na(td) <- 2:3
td.set_na(range(2, 4))

# R: td
# r2py:entity:td_1
print(td)

# R: is.na(td)
# r2py:entity:is.na_1
is_na_td_final = td.is_na()
vals_na_final = "  ".join([str(x).upper() for x in is_na_td_final])
print(f"      [1] {vals_na_final}")