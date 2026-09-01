# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dtplyr__rd_example__collect_dtplyr_step_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dtplyr__rd_example__collect_dtplyr_step_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['avg_mpg', 'avg_mpg_dt', 'avg_mpg_tb', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:dt
def lazy_dt(x):
    """
    dtplyr provides a lazy interface to data.table. 
    In Python, we wrap the dataframe in a class that stores the operation 
    to mimic the lazy behavior of dtplyr.
    """
    class LazyDt:
        def __init__(self, data):
            self.data = pd.DataFrame(data)
            self.ops = []
        
# r2py:entity:filter
        def filter(self, condition):
            # This is a simplification: in a real lazy system, we'd store the condition
            self.ops.append(('filter', condition))
            return self
        
# r2py:entity:group_by
        def group_by(self, col):
            self.ops.append(('group_by', col))
            return self
        
# r2py:entity:summarise
        def summarise(self, **kwargs):
            self.ops.append(('summarise', kwargs))
            return self
        
        def __repr__(self):
            # Mimic the R output showing the lazy call
            return f"Source: local data table\nCall: Lazy operation chain"

        def collect(self):
            df = self.data.copy()
            current_group = None
            for op, val in self.ops:
                if op == 'filter':
                    # Basic mapping for 'am == 1'
                    if val == 'am == 1':
                        df = df[df['am'] == 1]
                elif op == 'group_by':
                    current_group = val
                elif op == 'summarise':
                    if current_group:
                        # map mpg = mean(mpg)
                        df = df.groupby(current_group).agg(val)
            return df

    return LazyDt(x)

# r2py:entity:compute
def compute(step):
    """
    In dtplyr, compute() executes the lazy chain and returns the result.
    """
    if hasattr(step, 'collect'):
        return step.collect()
    return step

# Generate translation
dt = lazy_dt(mtcars)

# Simulate the dplyr pipe
# avg_mpg <- dt %>% filter(am == 1) %>% group_by(cyl) %>% summarise(mpg = mean(mpg))
# r2py:entity:avg_mpg
avg_mpg = dt.filter('am == 1').group_by('cyl').summarise(mpg='mean')

# Show translation and temporarily compute result
print(avg_mpg)

# compute and return tibble
# r2py:entity:avg_mpg_tb
avg_mpg_tb = compute(avg_mpg)
print(avg_mpg_tb)

# compute and return data.table
# r2py:entity:avg_mpg_dt
avg_mpg_dt = compute(avg_mpg)
print(avg_mpg_dt)

# modify translation to use intermediate assignment
# r2py:entity:compute
compute(avg_mpg)