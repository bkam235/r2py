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

# train.idx is already provided by data_shim as a list of 1-based indices.
# Convert 1-based indices to 0-based for Python indexing.
train_idx_0based = [i - 1 for i in train.idx]

# iris.train <- iris[train.idx, ]
iris_train = iris.iloc[train_idx_0based].copy()

# iris.test <- iris[-train.idx, ]
iris_test = iris.drop(iris.index[train_idx_0based]).copy()

def csrf(formula, training_data, test_data, params1, params2):
    """
    Simplified implementation of the ranger::csrf function.
    csrf usually compares two sets of parameters and returns the OOB error 
    and test error for each.
    """
    # Split formula: 'Species ~ .'
    target_col = formula.split('~')[0].strip()
    
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    y_test = test_data[target_col]

    results = []
    for params in [params1, params2]:
        # Map ranger params to sklearn: num.trees -> n_estimators, mtry -> max_features
        n_estimators = params.get('num.trees', 500)
        max_features = params.get('mtry', 'sqrt')
        
        # oob_score=True approximates the OOB error tracking in ranger
        rf = RandomForestClassifier(
            n_estimators=n_estimators, 
            max_features=max_features, 
            oob_score=True,
            random_state=42
        )
        rf.fit(X_train, y_train)
        
        oob_error = 1 - rf.oob_score_
        test_error = 1 - rf.score(X_test, y_test)
        results.append({'oob_error': oob_error, 'test_error': test_error})
    
    return results

# Run case-specific RF
# csrf(Species ~ ., training_data = iris.train, test_data = iris.test, 
#      params1 = list(num.trees = 50, mtry = 4), 
#      params2 = list(num.trees = 5))
csrf_result = csrf(
    formula='Species ~ .', 
    training_data=iris_train, 
    test_data=iris_test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)

# The original R code prints the output of csrf implicitly.
print(csrf_result)