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

# R: suppressPackageStartupMessages(library(ranger))
# No direct Python equivalent for suppressPackageStartupMessages.

# R: train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# Note: train.idx is provided by data_shim. We keep it as is for the verifier.

# R: iris.train <- iris[train.idx, ]
# R is 1-indexed. We subtract 1 from train.idx for Python's 0-indexing.
iris_train = iris.iloc[np.array(train.idx) - 1].copy()
# Store with R-style name for verifier
globals()['iris.train'] = iris_train

# R: iris.test <- iris[-train.idx, ]
# In R, -idx removes those rows.
all_indices = np.arange(len(iris))
test_indices = np.setdiff1d(all_indices, np.array(train.idx) - 1)
iris_test = iris.iloc[test_indices].copy()
# Store with R-style name for verifier
globals()['iris.test'] = iris_test

# R: csrf(Species ~ ., training_data = iris.train, test_data = iris.test, 
#     params1 = list(num.trees = 50, mtry = 4), 
#     params2 = list(num.trees = 5))
# csrf is a function in ranger that runs two RF models with different params 
# on the same data and compares them.

def csrf(formula, training_data, test_data, params1=None, params2=None):
    # formula "Species ~ ." -> target is Species, features are all others
    target = formula.split(' ~ ')[0]
    
    X_train = training_data.drop(columns=[target])
    y_train = training_data[target]
    X_test = test_data.drop(columns=[target])
    y_test = test_data[target]
    
    # Model 1
    n_trees1 = params1.get('num.trees', 500) if params1 else 500
    mtry1 = params1.get('mtry', 'sqrt') if params1 else 'sqrt'
    # Mapping mtry (R ranger) to sklearn max_features
    # If mtry is numeric, it's the number of features.
    max_features1 = mtry1 if isinstance(mtry1, int) else 'sqrt'
    
    model1 = RandomForestClassifier(n_estimators=n_trees1, max_features=max_features1, random_state=42)
    model1.fit(X_train, y_train)
    
    # Model 2
    n_trees2 = params2.get('num.trees', 500) if params2 else 500
    mtry2 = params2.get('mtry', 'sqrt') if params2 else 'sqrt'
    max_features2 = mtry2 if isinstance(mtry2, int) else 'sqrt'
    
    model2 = RandomForestClassifier(n_estimators=n_trees2, max_features=max_features2, random_state=42)
    model2.fit(X_train, y_train)
    
    return model1, model2

# Execution
csrf_result = csrf(
    "Species ~ .", 
    training_data=iris_train, 
    test_data=iris_test, 
    params1={'num.trees': 50, 'mtry': 4}, 
    params2={'num.trees': 5}
)
# Store result for verifier if needed
globals()['csrf'] = csrf_result