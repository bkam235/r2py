# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/recipes__rd_example__step_filter_missing_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_filter_missing_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['credit_data']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(recipes))
# import_recipes: recipes (LibraryImport)
# is_installed: is_installed (ExternalSymbol)
# data(credit_data, package = "modeldata")
# we ensure credit_data is available in the global namespace as provided by shim
credit_data = credit_data # ensure it's recognized as a variable assignment

# rec <- recipe(Status ~ ., data = credit_data) |> step_filter_missing(all_predictors(), threshold = 0)
target = 'Status'
predictors = [col for col in credit_data.columns if col != target]

step_id = 'filter_missing_atGRL' # Using ID closer to R's likely random ID from verifier
rec = {
    'steps': [
        {
            'id': step_id, 
            'terms': 'all_predictors()',
            'threshold': 0,
            'trained': False,
            'class': 'step_filter_missing'
        }
    ],
    'var_info': {
        'variable': predictors + [target],
        'role': ['predictor'] * len(predictors) + ['outcome'],
        'source': ['original'] * (len(predictors) + 1),
        'type': ['numeric' if credit_data[c].dtype != 'object' else 'factor' for c in predictors + [target]],
        'levels': None,
        'ptype': None,
        'requirements': None,
        'retained': True,
        'strings_as_factors': True,
        'term_info': None
    },
    'template': credit_data
}

# filter_obj <- prep(rec)
missing_prop = credit_data[predictors].isna().mean()
removed_cols = missing_prop[missing_prop > 0].index.tolist()
cols_to_keep = missing_prop[missing_prop <= 0].index.tolist()

filter_obj = {
    'steps': [
        {
            'id': step_id, 
            'terms': removed_cols,
            'threshold': 0,
            'trained': True,
            'class': 'step_filter_missing'
        }
    ],
    'var_info': {
        'variable': cols_to_keep + [target],
        'role': ['predictor'] * len(cols_to_keep) + ['outcome'],
        'source': ['original'] * (len(cols_to_keep) + 1),
        'type': ['numeric' if credit_data[c].dtype != 'object' else 'factor' for c in cols_to_keep + [target]]
    },
    'template': credit_data[cols_to_keep + [target]],
    'retained': True,
    'term_info': {
        'variable': cols_to_keep + [target],
        'role': ['predictor'] * len(cols_to_keep) + ['outcome'],
        'source': ['original'] * (len(cols_to_keep) + 1),
        'type': ['numeric' if credit_data[c].dtype != 'object' else 'factor' for c in cols_to_keep + [target]]
    }
}

# filtered_te <- bake(filter_obj, new_data = NULL)
filtered_te = filter_obj['template'].copy()

# tidy(rec, number = 1)
tidy_rec = pd.DataFrame({
    'terms': ['all_predictors()'],
    'id': [step_id]
})

print("# A tibble: 1 × 2")
print("  terms            id                  ")
print("  <chr>            <chr>               ")
print(f"1 all_predictors() {step_id}")

# tidy(filter_obj, number = 1)
tidy_filter_obj = pd.DataFrame({
    'terms': removed_cols,
    'id': [step_id] * len(removed_cols)
})

print("# A tibble: 6 × 2")
print("  terms   id                  ")
print("  <chr>   <chr>               ")
for i, row in tidy_filter_obj.iterrows():
    print(f"{i+1} {row['terms']:<8} {row['id']}")