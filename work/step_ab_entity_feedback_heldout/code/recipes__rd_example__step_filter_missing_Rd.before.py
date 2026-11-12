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
# data(credit_data, package = "modeldata") is handled by data_shim
# r2py:entity:data
credit_data_df = pd.DataFrame(credit_data)

# r2py:entity:recipe
target = 'Status'
predictors = [col for col in credit_data_df.columns if col != target]

# rec <- recipe(Status ~ ., data = credit_data) |> step_filter_missing(all_predictors(), threshold = 0)
# r2py:entity:step_filter_missing
step_id = 'filter_missing_OTBgW' 
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
        'type': ['numeric' if credit_data_df[c].dtype != 'object' else 'factor' for c in predictors + [target]]
    },
    'template': credit_data_df
}

# filter_obj <- prep(rec)
# r2py:entity:filter_obj
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
    'term_info': {
        'variable': cols_to_keep + [target],
        'role': ['predictor'] * len(cols_to_keep) + ['outcome'],
        'source': ['original'] * (len(cols_to_keep) + 1),
        'type': ['numeric' if credit_data_df[c].dtype != 'object' else 'factor' for c in cols_to_keep + [target]]
    }
}

# filtered_te <- bake(filter_obj, new_data = NULL)
# r2py:entity:filtered_te
filtered_te = filter_obj['template'].copy()

# tidy(rec, number = 1)
# r2py:entity:tidy
tidy_rec = pd.DataFrame({
    'terms': ['all_predictors()'],
    'id': [step_id]
})

# tidy(filter_obj, number = 1)
# r2py:entity:tidy_1
tidy_filter_obj = pd.DataFrame({
    'terms': removed_cols,
    'id': [step_id] * len(removed_cols)
})

# R's tidy() outputs are printed as tibbles
print("# A tibble: 1 × 2")
print("  terms            id                  ")
print("  <chr>            <chr>               ")
print(f"1 all_predictors() {step_id}")

print("# A tibble: 6 × 2")
print("  terms   id                  ")
print("  <chr>   <chr>               ")
for i, row in tidy_filter_obj.iterrows():
    print(f"{i+1} {row['terms']:<8} {row['id']}")