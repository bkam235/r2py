# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/recipes__rd_example__step_rm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_rm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import random
import string

def rand_id(prefix="step", length=5):
    candidates = string.ascii_letters + string.digits
    res = ''.join(random.choices(candidates, k=length))
    return f"{prefix}_{res}"

# r2py:entity:rec
class Recipe:
    def __init__(self, formula, data=None):
        self.formula = formula
        self.data = data
        self.steps = []
        
        parts = formula.split('~')
        self.outcome = parts[0].strip()
        self.predictors = [p.strip() for p in parts[1].split('+')]
        
        # Original variables in the recipe
        self.var_info = pd.DataFrame({
            'variable': self.predictors + [self.outcome],
            'role': ['predictor'] * len(self.predictors) + ['outcome'],
            'source': ['original'] * (len(self.predictors) + 1)
        })
        self.term_info = self.var_info.copy()

    # r2py:entity:step_rm
# r2py:entity:step_rm
    def step_rm(self, terms_selector):
        # In R, terms_selector (like contains("gen")) is evaluated against current vars
        # But here we evaluate it against all columns available in the training data if provided, 
        # or the current recipe terms.
        all_cols = self.term_info['variable'].tolist()
        removals = [col for col in all_cols if terms_selector(col)]
        
        step = {
            'operation': 'rm',
            'type': 'rm',
            'trained': False,
            'skip': False,
            'id': rand_id("rm"),
            'removals': removals
        }
        self.steps.append(step)
        return self

    # r2py:entity:smaller_set_1
# r2py:entity:smaller_set_1
    def prep(self, training=None):
        if training is not None:
            self.training_data = training
            current_terms = self.term_info['variable'].tolist()
            for step in self.steps:
                step['trained'] = True
                if step['operation'] == 'rm':
                    current_terms = [c for c in current_terms if c not in step['removals']]
            
            self.term_info = self.term_info[self.term_info['variable'].isin(current_terms)].copy()
        return self

    # r2py:entity:filtered_te
# r2py:entity:filtered_te
    def bake(self, new_data):
        # Bake returns the variables remaining in term_info
        cols_to_keep = self.term_info['variable'].tolist()
        # R's bake keeps the rows of new_data exactly as they are
        return new_data[cols_to_keep].reset_index(drop=True)

def contains(pattern):
    return lambda x: pattern in x

# r2py:entity:rec
def recipe(formula, data=None):
    return Recipe(formula, data)

# r2py:entity:smaller_set_1
def prep(rec, training=None):
    return rec.prep(training)

# r2py:entity:filtered_te
def bake(rec, new_data):
    return rec.bake(new_data)

# r2py:entity:tidy
def tidy(rec, number=None):
    if number is not None:
        idx = number - 1
        if idx < 0 or idx >= len(rec.steps):
            return None
        step = rec.steps[idx]
        if step['operation'] == 'rm':
            return pd.DataFrame({
                'terms': step['removals'],
                'id': [step['id']] * len(step['removals'])
            })
    
    return pd.DataFrame({
        'number': range(1, len(rec.steps) + 1),
        'operation': [s['operation'] for s in rec.steps],
        'type': [s['type'] for s in rec.steps],
        'trained': [s['trained'] for s in rec.steps],
        'skip': [s['skip'] for s in rec.steps],
        'id': [s['id'] for s in rec.steps]
    })

# --- Main Script ---

# data(biomass, package = "modeldata")
# r2py:entity:data
biomass_df = pd.DataFrame(biomass)

# biomass_tr <- biomass[biomass$dataset == "Training", ]
# r2py:entity:biomass_tr
biomass_tr = biomass_df[biomass_df['dataset'] == 'Training'].copy()
# biomass_te <- biomass[biomass$dataset == "Testing", ]
# r2py:entity:biomass_te
biomass_te = biomass_df[biomass_df['dataset'] == 'Testing'].copy()

# rec <- recipe(HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur, data = biomass_tr)
# r2py:entity:rec
rec = recipe("HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur", data=biomass_tr)

# smaller_set <- rec |> step_rm(contains("gen"))
# r2py:entity:smaller_set
smaller_set = rec.step_rm(contains("gen"))

# smaller_set <- prep(smaller_set, training = biomass_tr)
# r2py:entity:smaller_set_1
smaller_set = prep(smaller_set, training=biomass_tr)

# filtered_te <- bake(smaller_set, biomass_te)
# r2py:entity:filtered_te
filtered_te = bake(smaller_set, biomass_te)

print(filtered_te)

# tidy(smaller_set, number = 1)
# r2py:entity:tidy
tidy_results = tidy(smaller_set, number=1)
print(tidy_results)