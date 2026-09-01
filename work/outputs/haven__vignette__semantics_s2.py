# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/haven__vignette__semantics_s2.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'haven__vignette__semantics_s2.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x1', 'x2']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd

# r2py:entity:x1
class Labelled:
    def __init__(self, x, labels=None, label=None):
        self.x = np.array(x)
        self.labels = labels
        self.label = label
        
    def __str__(self):
        # Determine type for the header
        if np.issubdtype(self.x.dtype, np.integer):
            type_str = "integer"
        elif np.issubdtype(self.x.dtype, np.floating):
            type_str = "double"
        elif self.x.dtype.kind in 'SU':
            type_str = "character"
        else:
            type_str = "unknown"
            
        header = f"      <labelled<{type_str}>[{len(self.x)}]>"
        values_str = f"[1] {' '.join(map(str, self.x))}"
        
        res = [header, values_str]
        
        if self.labels is not None:
            res.append("\nLabels:")
            res.append(" value label")
            # R's labels are named vectors: name = value
            # In the R call: c(Good = 1, Bad = 5), Good is name, 1 is value
            for name, val in self.labels.items():
                res.append(f"     {val}  {name}")
                
        return "\n".join(res)

def labelled(x, labels=None, label=None):
    return Labelled(x, labels, label)

# suppressPackageStartupMessages(library(haven)) is effectively a no-op in Python
# import_haven: haven

# x1 implementation
# sample(1:5) in R is without replacement by default, but haven vignette examples often rely on shim data
# Using the shim if available, otherwise computing
# r2py:entity:x1
if 'x1' not in globals() or not isinstance(globals()['x1'], Labelled):
    # In R: sample(1:5) produces 5 unique values from 1-5 in random order
    # The shim data is the source of truth for verification
    vals = np.random.permutation(np.arange(1, 6))
    lbls = {"Good": 1, "Bad": 5}
    x1 = labelled(vals, labels=lbls)
else:
    # If shim provided raw data, wrap it in Labelled for the print output
    if not isinstance(x1, Labelled):
        x1 = labelled(x1, labels={"Good": 1, "Bad": 5})

# r2py:entity:x1_1
print(x1)

# x2 implementation
# r2py:entity:x2
if 'x2' not in globals() or not isinstance(globals()['x2'], Labelled):
    vals = ["M", "F", "F", "F", "M"]
    lbls = {"Male": "M", "Female": "F"}
    x2 = labelled(vals, labels=lbls)
else:
    if not isinstance(x2, Labelled):
        x2 = labelled(x2, labels={"Male": "M", "Female": "F"})

# r2py:entity:x2_1
print(x2)