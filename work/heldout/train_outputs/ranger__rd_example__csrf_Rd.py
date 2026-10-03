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
from ranger import Ranger # Note: Using a hypothetical wrapper or similar Random Forest implementation
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Data preparation
d = pd.DataFrame(np.load(pd.read_csv('https://gist.githubusercontent.com/netj treetops/raw/iris.csv'))) # Loading iris
# Since iris is standard, using seaborn/sklearn load
from sklearn.datasets import load_iris
iris_data = load_iris()
d = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
d['Species'] = iris_data.target

# train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# r2py:entity:train.idx
train_idx = np.random.choice(d.index, int(2/3 * len(d)), replace=False)

# iris.train <- iris[train.idx, ]
# iris.test <- iris[-train.idx, ]
# r2py:entity:iris.train
iris_train = d.loc[train_idx]
# r2py:entity:iris.test
iris_test = d.drop(train_idx)

# r2py:entity:csrf
# Define X and y
X_train = iris_train.drop('Species', axis=1)
y_train = iris_train['Species']
X_test = iris_test.drop('Species', axis=1)
y_test = iris_test['Species']

# The 'csrf' function in the R snippet appears to be a custom wrapper for ranger 
# that compares two models (training vs test/different params).
# params1 = list(num.trees = 50, mtry = 4)
model1 = RandomForestClassifier(n_estimators=50, max_features=4, random_state=42)
model1.fit(X_train, y_train)
pred1 = model1.predict(X_test)
acc1 = accuracy_score(y_test, pred1)

# params2 = list(num.trees = 5)
model2 = RandomForestClassifier(n_estimators=5, random_state=42)
model2.fit(X_train, y_train)
pred2 = model2.predict(X_test)
acc2 = accuracy_score(y_test, pred2)

print(f"Accuracy Model 1: {acc1}")
print(f"Accuracy Model 2: {acc2}")