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
from sklearn.metrics import accuracy_score

# iris.train <- iris[train.idx, ]
# Note: train.idx from shim is 1-based indexing from R.
# Convert to 0-based indexing for pandas.
train_idx_0 = [i - 1 for i in train.idx]
iris_train = iris.iloc[train_idx_0].copy()

# iris.test <- iris[-train.idx, ]
iris_test = iris.drop(iris.index[train_idx_0]).copy()

def csrf(formula, training_data, test_data, params1, params2):
    """
    Mimics ranger::csrf by training two RF models with different parameters
    and evaluating them on the test set.
    """
    # Parse formula 'Species ~ .'
    target_col = formula.split('~')[0].strip()
    
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    y_test = test_data[target_col]
    
    # Model 1
    model1 = RandomForestClassifier(
        n_estimators=params1.get('num.trees', 100),
        max_features=params1.get('mtry', 'sqrt'),
        random_state=42
    )
    model1.fit(X_train, y_train)
    pred1 = model1.predict(X_test)
    acc1 = accuracy_score(y_test, pred1)
    
    # Model 2
    model2 = RandomForestClassifier(
        n_estimators=params2.get('num.trees', 100),
        max_features=params2.get('mtry', 'sqrt'),
        random_state=42
    )
    model2.fit(X_train, y_train)
    pred2 = model2.predict(X_test)
    acc2 = accuracy_score(y_test, pred2)
    
    print(f"Model 1 (num.trees={params1.get('num.trees')}): Accuracy = {acc1}")
    print(f"Model 2 (num.trees={params2.get('num.trees')}): Accuracy = {acc2}")
    return acc1, acc2

# Run case-specific RF
csrf(
    "Species ~ .", 
    training_data=iris_train, 
    test_data=iris_test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)