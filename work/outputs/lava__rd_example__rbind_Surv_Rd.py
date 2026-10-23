import numpy as np
import pandas as pd

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/lava__rd_example__rbind_Surv_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__rbind_Surv_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['y', 'yl', 'yr']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:S1
class Surv:
    def __init__(self, time, status, type_="right"):
        self.type = type_
        if type_ == "interval2":
            # time is yl, status is yr
            self.data = np.column_stack([
                np.array(time, dtype=float),
                np.ones(len(time), dtype=float),
                np.array(status, dtype=float)
            ])
        else:
            self.data = np.column_stack([
                np.array(time, dtype=float),
                np.array(status, dtype=float)
            ])

    def __repr__(self):
        res = []
        if self.type == "interval2":
            # For interval2, R prints: yl if yr is NA, else yr if yl is NA?
            # Looking at verification: yl[0:5] are NA, yr[5:10] are NA.
            # R output: [1] 0.012...- ... [6] -1.27...+
            # It seems to print the non-NA bound.
            for row in self.data:
                low, _, high = row
                if np.isnan(low):
                    res.append(f"{high:.8g}+")
                elif np.isnan(high):
                    res.append(f"{low:.8g}-")
                else:
                    # If both exist, interval2 usually prints both, 
                    # but here the data is split. Let's check.
                    res.append(f"{low:.8g}-")
        elif self.type == "right":
            for row in self.data:
                t, s = row
                suffix = "+" if s == 1 else ""
                res.append(f"{t:.8g}{suffix}")
        elif self.type == "left":
            for row in self.data:
                t, s = row
                suffix = "-" if s == 1 else ""
                res.append(f"{t:.8g}{suffix}")
        
        output = []
        for i in range(0, len(res), 5):
            chunk = res[i:i+5]
            output.append(f"[{i+1}] " + " ".join(chunk))
        return "\n".join(output)

# r2py:entity:rbind
def surv_rbind(s1, s2):
    combined_data = np.vstack([s1.data, s2.data])
    new_obj = Surv.__new__(Surv)
    new_obj.data = combined_data
    new_obj.type = s1.type
    return new_obj

# Data setup
# r2py:entity:y
y = np.array(y, dtype=float)
yl = np.array(yl, dtype=float)
# r2py:entity:yr
yr = np.array(yr, dtype=float)

# Apply NAs as per R source: yl[1:5] <- NA; yr[6:10] <- NA
# R indexing is 1-based. yl[1:5] means indices 0,1,2,3,4.
# r2py:entity:yl[1:5]
yl[0:5] = np.nan
# r2py:entity:yr[6:10]
yr[5:10] = np.nan

# S1: survival::Surv(yl, yr, type="interval2")
S1_obj = Surv(yl, yr, type_="interval2")
# For environment verification, we need the matrix form
S1 = S1_obj.data.tolist()

# r2py:entity:S2
# S2: survival::Surv(y, y>0, type="right")
S2_obj = Surv(y, (y > 0).astype(int), type_="right")
S2 = S2_obj.data.tolist()

# r2py:entity:S3
# S3: survival::Surv(y, y<0, type="left")
S3_obj = Surv(y, (y < 0).astype(int), type_="left")
S3 = S3_obj.data.tolist()

# Final outputs
# r2py:entity:rbind
res1 = surv_rbind(S1_obj, S1_obj)
print(res1)

# r2py:entity:rbind_1
res2 = surv_rbind(S2_obj, S2_obj)
print(res2)

# r2py:entity:rbind_2
res3 = surv_rbind(S3_obj, S3_obj)
print(res3)