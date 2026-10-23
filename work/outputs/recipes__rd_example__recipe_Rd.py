# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__recipe_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__recipe_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

def suppressPackageStartupMessages(expr):
    return expr

# r2py:entity:recipe
class Recipe:
    def __init__(self, x, data=None):
        self.steps = []
        self.var_info = pd.DataFrame()
        self.template = None
        
        if isinstance(x, str) and '~' in x:
            formula = x
            self.template = data.copy() if data is not None else None
            lhs, rhs = formula.split('~')
            lhs = lhs.strip()
            rhs_vars = [v.strip() for v in rhs.split('+')]
            
            # Handle multivariate LHS
            lhs_vars = [v.strip() for v in lhs.split('+')] if '+' in lhs else [lhs]
            
            vars_all = lhs_vars + rhs_vars
            self.var_info = pd.DataFrame({
                'variable': vars_all,
                'role': ['outcome'] * len(lhs_vars) + ['predictor'] * len(rhs_vars),
                'type': ['numeric'] * len(vars_all)
            })
            
            if self.template is not None:
                for col in self.template.columns:
                    if col not in vars_all:
                        self.var_info = pd.concat([self.var_info, pd.DataFrame({
                            'variable': [col], 
                            'role': ['id variable'], 
                            'type': ['numeric' if np.issubdtype(self.template[col].dtype, np.number) else 'nominal']
                        })], ignore_index=True)
        
        elif isinstance(x, (pd.DataFrame, dict)):
            df = pd.DataFrame(x) if isinstance(x, dict) else x
            self.template = df.copy()
            self.var_info = pd.DataFrame({
                'variable': df.columns,
                'role': ['id variable'] * len(df.columns),
                'type': ['numeric' if np.issubdtype(df[col].dtype, np.number) else 'nominal' for col in df.columns]
            })

    def __repr__(self):
        # Attempt to mimic R recipe output
        res = "Recipe\n  Var Info:\n"
        res += self.var_info.to_string(index=False)
        res += f"\n  Steps: {len(self.steps)}"
        return res

def all_numeric_predictors(recipe):
    return recipe.var_info[(recipe.var_info['role'] == 'predictor') & (recipe.var_info['type'] == 'numeric')]['variable'].tolist()

# r2py:entity:step_normalize
def step_normalize(recipe, terms, role=None):
    recipe.steps.append({'step': 'normalize', 'terms': terms, 'role': role})
    return recipe

# r2py:entity:step_spatialsign
def step_spatialsign(recipe, terms, role='predictor'):
    recipe.steps.append({'step': 'spatialsign', 'terms': terms, 'role': role})
    return recipe

# r2py:entity:step_center
def step_center(recipe, terms, role=None):
    recipe.steps.append({'step': 'center', 'terms': terms, 'role': role})
    return recipe

# r2py:entity:step_scale
def step_scale(recipe, terms, role=None):
    recipe.steps.append({'step': 'scale', 'terms': terms, 'role': role})
    return recipe

# r2py:entity:update_role
def update_role(recipe, *vars_to_update, new_role='predictor', old_role=None):
    recipe.var_info.loc[recipe.var_info['variable'].isin(vars_to_update), 'role'] = new_role
    return recipe

# r2py:entity:recipe
def recipe(x, data=None):
    return Recipe(x, data=data)

# Start script execution
# r2py:entity:data
biomass_df = pd.DataFrame(biomass)

# split data
# r2py:entity:biomass_tr
biomass_tr = biomass_df[biomass_df['dataset'] == 'Training'].copy()
# r2py:entity:biomass_te
biomass_te = biomass_df[biomass_df['dataset'] == 'Testing'].copy()

# Formula example with single outcome
# r2py:entity:rec
rec = recipe("HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur", data=biomass_tr)

# Preprocessing steps
numeric_preds = all_numeric_predictors(rec)
# r2py:entity:step_normalize
rec = step_normalize(rec, numeric_preds)
# r2py:entity:sp_signed
sp_signed = step_spatialsign(rec, numeric_preds)
print(sp_signed)

# Formula multivariate example
# r2py:entity:multi_y
multi_y = recipe("carbon + hydrogen ~ oxygen + nitrogen + sulfur", data=biomass_tr)
numeric_preds_multi = all_numeric_predictors(multi_y)
# r2py:entity:multi_y_1
multi_y = step_center(multi_y, numeric_preds_multi)
# r2py:entity:step_scale
multi_y = step_scale(multi_y, numeric_preds_multi)

# Example using update_role instead of formula
# r2py:entity:rec_1
rec_role = recipe(biomass_tr)
# r2py:entity:update_role
rec_role = update_role(rec_role, 'carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur', new_role='predictor')
# r2py:entity:update_role_1
rec_role = update_role(rec_role, 'HHV', new_role='outcome')
# r2py:entity:update_role_2
rec_role = update_role(rec_role, 'sample', new_role='id variable')
# r2py:entity:update_role_3
rec_role = update_role(rec_role, 'dataset', new_role='splitting indicator')
print(rec_role)