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

# train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# train.idx is provided by the shim.

# iris.train <- iris[train.idx, ]
# R's train.idx is 1-based. Convert to 0-based for pandas .iloc
train_idx_0 = [i - 1 for i in train.idx]
iris_train = iris.iloc[train_idx_0]

# iris.test <- iris[-train.idx, ]
iris_test = iris.drop(iris.index[train_idx_0])

def csrf(formula, training_data, test_data, params1, params2):
    """
    Mimics the R ranger::csrf function which performs a 
    cross-validation style check between two sets of hyperparameters.
    """
    # Parse formula "Species ~ ."
    target_col = formula.split('~')[0].strip()
    
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    y_test = test_data[target_col]
    
    # params1: num.trees -> n_estimators, mtry -> max_features
    model1 = RandomForestClassifier(
        n_estimators=params1.get('num.trees', 500),
        max_features=params1.get('mtry', 'sqrt'),
        random_state=42
    )
    model1.fit(X_train, y_train)
    score1 = model1.score(X_test, y_test)
    
    # params2
    model2 = RandomForestClassifier(
        n_estimators=params2.get('num.trees', 500),
        max_features=params2.get('mtry', 'sqrt'),
        random_state=42
    )
    model2.fit(X_train, y_train)
    score2 = model2.score(X_test, y_test)
    
    return score1, score2

# Run case-specific RF
csrf(
    "Species ~ .", 
    training_data=iris_train, 
    test_data=iris_test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)