# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ranger__rd_example__csrf_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__csrf_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# R: train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# The data shim already provides train.idx from R. 
# R's train.idx is 1-based.
train_idx_0based = [i - 1 for i in train_idx]

# R: iris.train <- iris[train.idx, ]
# r2py:entity:iris.train
iris_train = iris.iloc[train_idx_0based].copy()

# R: iris.test <- iris[-train.idx, ]
# r2py:entity:iris.test
iris_test = iris.drop(iris.index[train_idx_0based]).copy()

# R: csrf(Species ~ ., training_data = iris.train, test_data = iris.test, 
#      params1 = list(num.trees = 50, mtry = 4), 
#      params2 = list(num.trees = 5))
# r2py:entity:csrf
def csrf(formula, training_data, test_data, params1, params2):
    # Split formula 'Species ~ .'
    target_col = formula.split('~')[0].strip()
    
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    y_test = test_data[target_col]
    
    # Model 1
    rf1 = RandomForestClassifier(
        n_estimators=params1.get('num.trees', 500), 
        max_features=params1.get('mtry', 'sqrt'), 
        random_state=42
    )
    rf1.fit(X_train, y_train)
    
    # Model 2
    rf2 = RandomForestClassifier(
        n_estimators=params2.get('num.trees', 500), 
        max_features=params2.get('mtry', 'sqrt'), 
        random_state=42
    )
    rf2.fit(X_train, y_train)
    
    return rf1, rf2

# Execute the logic as in the R script
csrf(
    "Species ~ .", 
    training_data=iris_train, 
    test_data=iris_test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)