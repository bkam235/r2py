# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__vignette__Roles_chunk11.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__vignette__Roles_chunk11.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
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
        # Default roles: in recipes, usually everything is a 'predictor' except target
        self.var_info = pd.DataFrame({
            'variable': self.data.columns,
            'role': 'predictor'
        })

# r2py:entity:step_dummy
    def step_dummy(self, vars, role='predictor'):
        # Store the step definition
        self.steps.append({'type': 'dummy', 'vars': vars, 'role': role})
        return self

# r2py:entity:prep
    def prep(self):
        # In this simplified version, prep just validates the pipeline
        # and determines the levels for the dummy variables
        self.trained_steps = []
        for step in self.steps:
            if step['type'] == 'dummy':
                for var in step['vars']:
                    levels = sorted(self.data[var].unique())
                    # R's step_dummy typically drops the first level (contr.treatment)
                    # So we store the levels that will become columns
                    dummy_cols = [f"{var}_{lvl}" for lvl in levels[1:]]
                    self.trained_steps.append({
                        'type': 'dummy', 
                        'var': var, 
                        'cols': dummy_cols, 
                        'role': step['role']
                    })
        return self

# r2py:entity:bake
    def bake(self, new_data=None, selection=None):
        data = self.data.copy() if new_data is None else new_data.copy()
        
        # Execute dummy steps
        for step in self.trained_steps:
            var = step['var']
            levels = sorted(self.data[var].unique())
            # Create dummies and drop first
            dummies = pd.get_dummies(data[var], prefix=var)
            # Align with R's treatment contrast (drop first)
            # We need to ensure we keep the same columns as determined in prep
            cols_to_keep = step['cols']
            # Filter dummies to match expected columns
            dummies = dummies[[c for c in dummies.columns if c in cols_to_keep]]
            
            data = pd.concat([data, dummies], axis=1)
            # Update var_info for new columns
            new_info = pd.DataFrame({
                'variable': cols_to_keep,
                'role': step['role']
            })
            self.var_info = pd.concat([self.var_info, new_info], ignore_index=True)

        # Handle selection based on role or predictor
        if selection is not None:
            if callable(selection):
                # Handle has_role() and all_predictors()
                selected_vars = selection(self.var_info)
                data = data[selected_vars]
            else:
                data = data[selection]
        
        return data

# r2py:entity:bake
def all_predictors(var_info):
    return var_info[var_info['role'] == 'predictor']['variable'].tolist()

# r2py:entity:bake_1
def has_role(role_name):
    def selector(var_info):
        return var_info[var_info['role'] == role_name]['variable'].tolist()
    return selector

# block 1
# recipe( ~ ., data = iris) |> step_dummy(Species) |> prep() |> bake(new_data = NULL, all_predictors()) |> dplyr::select(starts_with("Species")) |> names()
# r2py:entity:recipe
rec1 = Recipe(None, iris)
# r2py:entity:step_dummy
rec1.step_dummy(['Species'])
# r2py:entity:prep
rec1.prep()
# r2py:entity:bake
baked1 = rec1.bake(selection=all_predictors)
# dplyr::select(starts_with("Species"))
# r2py:entity:select
cols_first = [col for col in baked1.columns if col.startswith('Species')]
# r2py:entity:names
print(f"[1] {' '.join(map(repr, cols_first))}")

# block 2
# recipe( ~ ., data = iris) |> step_dummy(Species, role = "trousers") |> prep() |> bake(new_data = NULL, has_role("trousers")) |> names()
# r2py:entity:recipe_1
rec2 = Recipe(None, iris)
# r2py:entity:step_dummy_1
rec2.step_dummy(['Species'], role='trousers')
# r2py:entity:prep_1
rec2.prep()
# r2py:entity:bake_1
baked2 = rec2.bake(selection=has_role('trousers'))
# r2py:entity:names_1
cols_second = baked2.columns.tolist()
print(f"[1] {' '.join(map(repr, cols_second))}")