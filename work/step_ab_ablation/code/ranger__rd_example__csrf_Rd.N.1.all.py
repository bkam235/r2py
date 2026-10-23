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

# train.idx is provided by the shim (1-based index from R)
# Convert to 0-based indices for pandas
train_idx_0 = [i - 1 for i in train_idx]

# iris.train <- iris[train.idx, ]
iris_train = iris.iloc[train_idx_0].copy()

# iris.test <- iris[-train.idx, ]
iris_test = iris.drop(iris.index[train_idx_0]).copy()

# csrf is a wrapper that fits two models with different params and likely compares them.
# Formula: Species ~ .
X_train = iris_train.drop(columns=['Species'])
y_train = iris_train['Species']
X_test = iris_test.drop(columns=['Species'])
y_test = iris_test['Species']

# params1 = list(num.trees = 50, mtry = 4)
# In sklearn, max_features corresponds to mtry.
model1 = RandomForestClassifier(n_estimators=50, max_features=4, random_state=42)
model1.fit(X_train, y_train)

# params2 = list(num.trees = 5)
model2 = RandomForestClassifier(n_estimators=5, random_state=42)
model2.fit(X_train, y_train)

# The R csrf function typically returns a comparison of accuracy/error.
# Since we need to produce a result equivalent to the R call, we'll compute the scores.
score1 = model1.score(X_test, y_test)
score2 = model2.score(X_test, y_test)

# We assign the results to a variable that represents the output of the csrf call
csrf_result = {"model1_accuracy": score1, "model2_accuracy": score2}