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

# iris is already loaded by the data_shim
# train.idx is already loaded by the data_shim

# iris.train <- iris[train.idx, ]
# Note: train.idx from R is 1-indexed. Convert to 0-indexed for pandas.
idx_0 = [i - 1 for i in train.idx]
iris.train = iris.iloc[idx_0].copy()

# iris.test <- iris[-train.idx, ]
# Create a set for efficient lookup
idx_set = set(idx_0)
iris.test = iris.drop(index=idx_0).copy()

def csrf(formula, training_data, test_data, params1=None, params2=None):
    """
    Simulates the R ranger::csrf behavior.
    R's Species ~ . means Species is the target, others are features.
    """
    # Extract target name from formula string "Species ~ ."
    target_col = formula.split('~')[0].strip()
    
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    y_test = test_data[target_col]
    
    results = {}
    
    # Model 1
    p1 = params1 if params1 else {}
    # num.trees -> n_estimators, mtry -> max_features
    n_trees1 = p1.get('num.trees', 500)
    mtry1 = p1.get('mtry', 'sqrt') 
    # Handle mtry as integer or 'sqrt'
    model1 = RandomForestClassifier(n_estimators=n_trees1, max_features=mtry1, random_state=42)
    model1.fit(X_train, y_train)
    results['model1_acc'] = accuracy_score(y_test, model1.predict(X_test))
    
    # Model 2
    p2 = params2 if params2 else {}
    n_trees2 = p2.get('num.trees', 500)
    mtry2 = p2.get('mtry', 'sqrt')
    model2 = RandomForestClassifier(n_estimators=n_trees2, max_features=mtry2, random_state=42)
    model2.fit(X_train, y_train)
    results['model2_acc'] = accuracy_score(y_test, model2.predict(X_test))
    
    return results

# csrf(Species ~ ., training_data = iris.train, test_data = iris.test, 
#      params1 = list(num.trees = 50, mtry = 4), 
#      params2 = list(num.trees = 5))
csrf_result = csrf(
    formula="Species ~ .", 
    training_data=iris.train, 
    test_data=iris.test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)