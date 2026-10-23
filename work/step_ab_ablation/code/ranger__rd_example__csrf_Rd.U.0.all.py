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

# train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# Note: train.idx is provided by the shim. If it were calculated:
# train_idx = np.random.choice(len(iris), int(2/3 * len(iris)), replace=False)

# Adjust R's 1-based indices to Python's 0-based indices
train_idx_0 = [i - 1 for i in train_idx]

# iris.train <- iris[train.idx, ]
# r2py:entity:iris.train
iris_train = iris.iloc[train_idx_0].reset_index(drop=True)

# iris.test <- iris[-train.idx, ]
# r2py:entity:iris.test
iris_test = iris.drop(iris.index[train_idx_0]).reset_index(drop=True)

# r2py:entity:csrf
def csrf(formula, training_data, test_data, params1, params2):
    """
    Simulates the ranger::csrf function which compares two RF models 
    with different parameters on a test set.
    """
    # Separate target and features based on the formula 'Species ~ .'
    target_col = formula.split('~')[0].strip()
    
    X_train = training_data.drop(columns=[target_col])
    y_train = training_data[target_col]
    X_test = test_data.drop(columns=[target_col])
    y_test = test_data[target_col]
    
    # Model 1
    # mtry in R is max_features in sklearn
    # num.trees in R is n_estimators in sklearn
    clf1 = RandomForestClassifier(
        n_estimators=params1.get('num.trees', 100),
        max_features=params1.get('mtry', 'sqrt'),
        random_state=42
    )
    clf1.fit(X_train, y_train)
    pred1 = clf1.predict(X_test)
    acc1 = accuracy_score(y_test, pred1)
    
    # Model 2
    clf2 = RandomForestClassifier(
        n_estimators=params2.get('num.trees', 100),
        max_features=params2.get('mtry', 'sqrt'),
        random_state=42
    )
    clf2.fit(X_train, y_train)
    pred2 = clf2.predict(X_test)
    acc2 = accuracy_score(y_test, pred2)
    
    return acc1, acc2

# Run case-specific RF
# csrf(Species ~ ., training_data = iris.train, test_data = iris.test, 
#      params1 = list(num.trees = 50, mtry = 4), 
#      params2 = list(num.trees = 5))
csrf_results = csrf(
    formula='Species ~ .',
    training_data=iris_train,
    test_data=iris_test,
    params1={'num.trees': 50, 'mtry': 4},
    params2={'num.trees': 5}
)