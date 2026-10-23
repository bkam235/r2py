# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__step_factor2string_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_factor2string_Rd.r2py_data.json').read_text(encoding='utf-8'))
# r2py:entity:is_installed
# for _r2py_shim_n in ['Sacramento']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# --- Simulation of recipes package ---

# r2py:entity:rec
class Recipe:
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.steps = []
        # Simulate var_info and term_info based on the formula/data
        # In R, rec <- recipe(~ city + zip, data = Sacramento)
        # We extract the predictors from the formula "~ city + zip"
        predictors = [col for col in data.columns if col in formula]
        self.var_info = pd.DataFrame({
            'variable': predictors,
            'type': ['factor' if data[col].dtype == 'object' else 'numeric' for col in predictors],
            'role': ['predictor'] * len(predictors),
            'source': ['original'] * len(predictors)
        })
        self.term_info = self.var_info.copy()
        self.template = data.copy()
        self.retained = True

    def __repr__(self):
        return f"Recipe(steps={len(self.steps)}, var_info={self.var_info.to_dict('list')})"

# r2py:entity:step_factor2string
def step_factor2string(recipe, column):
    step = {
        'subclass': 'factor2string',
        'terms': column,
        'role': None,
        'trained': False,
        'columns': column,
        'skip': False,
        'id': 'step_factor2string_1'
    }
    recipe.steps.append(step)
    return recipe

# r2py:entity:make_string_1
def prep(recipe, training=None, strings_as_factors=False):
    # In R: prep fits the transformation
    if training is None:
        training = recipe.template
    
    # Update training data based on strings_as_factors
    tr_df = training.copy()
    
    for step in recipe.steps:
        if step['subclass'] == 'factor2string':
            col = step['terms']
            # Mark as trained
            step['trained'] = True
            # In R, this step changes the type in term_info
            recipe.term_info.loc[recipe.term_info['variable'] == col, 'type'] = 'string'
    
    # The result of prep is the recipe object itself (trained)
    return recipe

# r2py:entity:bake
def bake(recipe, new_data=None):
    # In R: bake applies the recipe. If new_data is NULL, it uses the training set (juice)
    if new_data is None:
        df = recipe.template.copy()
    else:
        df = new_data.copy()
    
    for step in recipe.steps:
        if step['subclass'] == 'factor2string':
            col = step['terms']
            df[col] = df[col].astype(str)
            
    return df

# --- Main Script ---

# data(Sacramento, package = "modeldata")
# r2py:entity:data
Sacramento = pd.DataFrame(Sacramento)

# rec <- recipe(~ city + zip, data = Sacramento)
# r2py:entity:rec
rec = Recipe("city + zip", Sacramento)

# make_string <- rec |> step_factor2string(city)
# r2py:entity:make_string
make_string = step_factor2string(rec, 'city')

# make_string <- prep(make_string, training = Sacramento, strings_as_factors = FALSE)
# r2py:entity:make_string_1
make_string = prep(make_string, training=Sacramento, strings_as_factors=False)

# make_string (print)
print(make_string)

# bake(make_string, new_data = NULL) |> head()
# r2py:entity:head
print(bake(make_string, new_data=None).head())

# Sacramento |> head()
# r2py:entity:head_1
print(Sacramento.head())