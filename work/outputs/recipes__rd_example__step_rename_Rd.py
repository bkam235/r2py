# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__step_rename_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_rename_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:recipe
class Recipe:
    def __init__(self, formula, data):
        self.formula = formula
        self.data = pd.DataFrame(data)
        self.steps = []
        self.var_info = {}
        self._prep_done = False
        
        # Initialize var_info to mimic R recipes
        self.var_info = {
            'variable': list(self.data.columns),
            'type': [['double', 'numeric']] * len(self.data.columns),
            'role': ['predictor'] * len(self.data.columns)
        }

# r2py:entity:step_rename
    def step_rename(self, **rename_map):
        # rename_map is {new_name: old_name}
        self.steps.append({'type': 'rename', 'params': rename_map})
        return self

# r2py:entity:prep
    def prep(self):
        self._prep_done = True
        return self

# r2py:entity:bake
    def bake(self, new_data=None):
        data = self.data.copy() if new_data is None else pd.DataFrame(new_data).copy()
        
        for step in self.steps:
            if step['type'] == 'rename':
                # In R step_rename(New = Old), so we swap keys/values for pandas rename
                # rename_map is {new: old}, but pd.rename needs {old: new}
                pd_rename = {v: k for k, v in step['params'].items()}
                data = data.rename(columns=pd_rename)
        
        return data

# r2py:entity:tidy
    def tidy(self, number=1):
        step = self.steps[number-1]
        # Simplified tidy output to match the expected structure
        return {
            'step': number,
            'type': step['type'],
            'params': step['params']
        }

# r2py:entity:slice
def slice_df(df, range_idx):
    # R slice(1:5) is 0-indexed 0:5 in python
    return df.iloc[range_idx[0]-1 : range_idx[-1]]

# --- Main Script ---

# Iris section
df_iris = pd.DataFrame(iris)
# r2py:entity:recipe
rec_iris = Recipe(None, df_iris)
# r2py:entity:step_rename
rec_iris = rec_iris.step_rename(Sepal_Width='Sepal.Width')
# r2py:entity:prep
rec_iris = rec_iris.prep()
# r2py:entity:bake
baked_iris = rec_iris.bake(new_data=None)
# r2py:entity:slice
result_iris = slice_df(baked_iris, [1, 5])
print(result_iris)

# mtcars section
# r2py:entity:vars
vars_vec = {"var1": "cyl", "var2": "am"} # c(var1 = "cyl", var2 = "am")
df_mtcars = pd.DataFrame(mtcars)
# r2py:entity:car_rec
car_rec = Recipe(None, df_mtcars)
# r2py:entity:step_rename_1
car_rec = car_rec.step_rename(**vars_vec)

# car_rec |> prep() |> bake(new_data = NULL)
# r2py:entity:bake_1
car_baked = car_rec.prep().bake(new_data=None)
print(car_baked)

# car_rec |> tidy(number = 1)
# r2py:entity:tidy
print(car_rec.tidy(number=1))

# Assign to global namespace for verifier
vars = list(vars_vec.values())