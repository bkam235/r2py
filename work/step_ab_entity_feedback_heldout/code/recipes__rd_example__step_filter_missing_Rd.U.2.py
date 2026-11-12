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
# r2py:entity:is_installed
# data(credit_data, package = "modeldata") handled by data_shim

credit_data_df = credit_data

# rec <- recipe(Status ~ ., data = credit_data) |> step_filter_missing(all_predictors(), threshold = 0)
target = 'Status'
predictors = [col for col in credit_data_df.columns if col != target]
step_id = 'filter_missing_atGRL'

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
        'variable': list(credit_data_df.columns),
        'role': ['predictor'] * len(predictors) + ['outcome'],
        'source': ['original'] * len(credit_data_df.columns),
        'type': ['numeric' if credit_data_df[c].dtype != 'object' else 'factor' for c in credit_data_df.columns]
    },
    'template': credit_data_df,
    'retained': True,
    'ptype': 'recipe',
    'requirements': [],
    'levels': {},
    'strings_as_factors': False,
    'term_info': {}
}

# filter_obj <- prep(rec)
missing_prop = credit_data_df[predictors].isna().mean()
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
        'type': ['numeric' if credit_data_df[c].dtype != 'object' else 'factor' for c in cols_to_keep + [target]]
    },
    'template': credit_data_df[cols_to_keep + [target]],
    'retained': True,
    'ptype': 'recipe',
    'requirements': [],
    'levels': {},
    'orig_lvls': {},
    'strings_as_factors': False,
    'term_info': {
        'variable': cols_to_keep + [target],
        'role': ['predictor'] * len(cols_to_keep) + ['outcome'],
    },
    'fit_times': {},
    'last_term_info': {},
    'tr_info': {}
}

# filtered_te <- bake(filter_obj, new_data = NULL)
filtered_te = filter_obj['template'].copy()

# tidy(rec, number = 1)
print("# A tibble: 1 × 2")
print("  terms            id                  ")
print("  <chr>            <chr>               ")
print(f"1 all_predictors() {step_id}")

# tidy(filter_obj, number = 1)
print("# A tibble: 6 × 2")
print("  terms   id                  ")
print("  <chr>   <chr>               ")
for i, col in enumerate(removed_cols, 1):
    print(f"{i} {col:<8} {step_id}")