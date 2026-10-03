# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import pandas as pd
import numpy as np
import re

class Period:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __repr__(self):
        res = []
        if self.hour > 0:
            res.append(f"{self.hour}H")
        if self.minute > 0:
            res.append(f"{self.minute}M")
        if self.second > 0 or not res:
            res.append(f"{self.second}S")
        return " ".join(res)

    def __str__(self):
        return self.__repr__()

def _parse_hms_logic(inputs, order):
    if isinstance(inputs, str):
        inputs = [inputs]
    elif not isinstance(inputs, (list, np.ndarray, pd.Series)):
        inputs = list(inputs)

    results = []
    for val in inputs:
        # Extract all numbers from the string
        nums = re.findall(r'\d+', str(val))
        
        # Assign numbers based on the requested order
        h, m, s = 0, 0, 0
        if order == "MS":
            if len(nums) >= 2:
                m, s = int(nums[0]), int(nums[1])
        elif order == "HM":
            if len(nums) >= 2:
                h, m = int(nums[0]), int(nums[1])
        elif order == "HMS":
            if len(nums) >= 3:
                h, m, s = int(nums[0]), int(nums[1]), int(nums[2])
            elif len(nums) == 2:
                h, m = int(nums[0]), int(nums[1])
            elif len(nums) == 1:
                h = int(nums[0])
        
        results.append(Period(hour=h, minute=m, second=s))
    return results

# r2py:entity:ms
def ms(*args, quiet=False, roll=False):
    # R's ... handles both vectors and multiple arguments
    inputs = []
    for arg in args:
        if isinstance(arg, (list, np.ndarray, pd.Series)):
            inputs.extend(arg)
        else:
            inputs.append(arg)
    
    return _parse_hms_logic(inputs, "MS")

# r2py:entity:hm
def hm(*args, quiet=False, roll=False):
    inputs = []
    for arg in args:
        if isinstance(arg, (list, np.ndarray, pd.Series)):
            inputs.extend(arg)
        else:
            inputs.append(arg)
            
    return _parse_hms_logic(inputs, "HM")

# r2py:entity:hms
def hms(*args, quiet=False, roll=False):
    inputs = []
    for arg in args:
        if isinstance(arg, (list, np.ndarray, pd.Series)):
            inputs.extend(arg)
        else:
            inputs.append(arg)
            
    return _parse_hms_logic(inputs, "HMS")

def format_r_vector(vec):
    # Simulates R's print output for vectors: [1] "val1" "val2"
    items = " ".join([f'"{str(x)}"' for x in vec])
    return f'[1] {items}'

# Execution
# r2py:entity:ms
res_ms = ms(["09:10", "09:02", "1:10"])
print(format_r_vector(res_ms))

# r2py:entity:ms_1
res_ms1 = ms("7 6")
print(format_r_vector(res_ms1))

# r2py:entity:ms_2
res_ms2 = ms("6,5")
print(format_r_vector(res_ms2))

# r2py:entity:hm
res_hm = hm(["09:10", "09:02", "1:10"])
print(format_r_vector(res_hm))

# r2py:entity:hm_1
res_hm1 = hm("7 6")
print(format_r_vector(res_hm1))

# r2py:entity:hm_2
res_hm2 = hm("6,5")
print(format_r_vector(res_hm2))

# r2py:entity:x
x = ["09:10:01", "09:10:02", "09:10:03"]
# r2py:entity:hms
res_hms = hms(x)
print(format_r_vector(res_hms))

# r2py:entity:hms_1
res_hms1 = hms("7 6 5", "3:23:::2", "2 : 23 : 33", "Finished in 9 hours, 20 min and 4 seconds")
print(format_r_vector(res_hms1))