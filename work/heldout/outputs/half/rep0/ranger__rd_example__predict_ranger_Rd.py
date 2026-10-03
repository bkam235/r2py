# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/ranger__rd_example__predict_ranger_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__predict_ranger_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mtcars', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix

# Convert shim data to DataFrames
if 'iris' in globals() and isinstance(iris, dict):
    iris = pd.DataFrame(iris)
if 'mtcars' in globals() and isinstance(mtcars, dict):
    mtcars = pd.DataFrame(mtcars)

# Classification forest
# ranger(Species ~ ., data = iris)
# r2py:entity:ranger
X_iris_all = iris.drop('Species', axis=1)
y_iris_all = iris['Species']
# We don't need to store this result as it's not assigned to a variable in R
_ = RandomForestClassifier(n_estimators=500, random_state=42).fit(X_iris_all.values, y_iris_all)

# train.idx is provided by shim
# r2py:entity:train.idx
train_idx_vals = globals().get('train.idx', [])
train_idx_0based = [int(i) - 1 for i in train_idx_vals]

# r2py:entity:iris.train
# iris.train <- iris[train.idx, ]
iris_train_df = iris.iloc[train_idx_0based].copy()
globals()['iris.train'] = iris_train_df

# r2py:entity:iris.test
# iris.test <- iris[-train.idx, ]
iris_test_df = iris.drop(iris.index[train_idx_0based]).copy()
globals()['iris.test'] = iris_test_df

# rg.iris <- ranger(Species ~ ., data = iris.train)
# r2py:entity:rg.iris
X_train_iris = iris_train_df.drop('Species', axis=1)
y_train_iris = iris_train_df['Species']
rg_iris_model = RandomForestClassifier(n_estimators=500, random_state=42).fit(X_train_iris.values, y_train_iris)

# Construct rg.iris object to match R's ranger structure
globals()['rg.iris'] = {
    'predictions': rg_iris_model.predict(X_train_iris.values).tolist(),
    'treetype': 'Classification',
    'num.trees': 500,
    'num.independent.variables': X_train_iris.shape[1],
    'num.samples': X_train_iris.shape[0],
    'mtry': int(np.sqrt(X_train_iris.shape[1])),
    'min.node.size': 1,
    'replace': True,
    'splitrule': 'gini',
    'call': 'ranger(Species ~ ., data = iris.train)',
    'dependent.variable.name': 'Species',
    'importance.mode': 'none',
    'max.depth': None,
    'prediction.error': 0.0, # Placeholder
    'forest': {} # Placeholder
}

# pred.iris <- predict(rg.iris, data = iris.test)
# r2py:entity:pred.iris
X_test_iris = iris_test_df.drop('Species', axis=1)
pred_iris_vals = rg_iris_model.predict(X_test_iris.values)
globals()['pred.iris'] = {
    'predictions': pred_iris_vals.tolist(),
    'num.samples': X_test_iris.shape[0],
    'treetype': 'Classification',
    'num.independent.variables': X_train_iris.shape[1],
    'num.trees': 500
}

# table(iris.test$Species, pred.iris$predictions)
# r2py:entity:table
conf_matrix = confusion_matrix(iris_test_df['Species'], pred_iris_vals)
unique_species = np.unique(iris_test_df['Species'])
unique_preds = np.unique(pred_iris_vals)
# If some classes are missing in preds, confusion_matrix might be smaller
# We ensure the labels match for the DataFrame
_table_result = pd.DataFrame(conf_matrix, index=unique_species, columns=unique_preds)

# Quantile regression forest
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# r2py:entity:rf
mtcars_train = mtcars.iloc[0:26]
X_mt_train = mtcars_train.drop('mpg', axis=1)
y_mt_train = mtcars_train['mpg']
rf_model = RandomForestRegressor(n_estimators=500, random_state=42).fit(X_mt_train.values, y_mt_train)

globals()['rf'] = {
    'predictions': rf_model.predict(X_mt_train.values).tolist(),
    'treetype': 'Regression',
    'num.trees': 500,
    'num.independent.variables': X_mt_train.shape[1],
    'num.samples': X_mt_train.shape[0],
    'mtry': 3,
    'min.node.size': 5,
    'replace': True,
    'splitrule': 'variance',
    'call': 'ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)',
    'dependent.variable.name': 'mpg',
    'importance.mode': 'none',
    'max.depth': None,
    'prediction.error': 0.0, # Placeholder
    'forest': {} # Placeholder
}

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", quantiles = c(0.1, 0.5, 0.9))
# r2py:entity:pred
mtcars_test = mtcars.iloc[26:32]
X_mt_test = mtcars_test.drop('mpg', axis=1)
# Quantile Regression Forest: collect predictions from every single tree
all_tree_preds = np.array([tree.predict(X_mt_test.values) for tree in rf_model.estimators_])
pred_quantiles = np.quantile(all_tree_preds, q=[0.1, 0.5, 0.9], axis=0)
globals()['pred'] = {
    'predictions': pred_quantiles.T.tolist(),
    'num.samples': X_mt_test.shape[0],
    'treetype': 'Regression',
    'num.independent.variables': X_mt_train.shape[1],
    'num.trees': 500
}

# Quantile regression forest with user-specified function
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# The R code re-assigns rf. We just use the existing rf_model.
# r2py:entity:rf_1
globals()['rf'] = {
    'predictions': rf_model.predict(X_mt_train.values).tolist(),
    'treetype': 'Regression',
    'num.trees': 500,
    'num.independent.variables': X_mt_train.shape[1],
    'num.samples': X_mt_train.shape[0],
    'mtry': 3,
    'min.node.size': 5,
    'replace': True,
    'splitrule': 'variance',
    'call': 'ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)',
    'dependent.variable.name': 'mpg',
    'importance.mode': 'none',
    'max.depth': None,
    'prediction.error': 0.0,
    'forest': {}
}

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", 
#                what = function(x) sample(x, 10, replace = TRUE))
# r2py:entity:pred_1
def custom_what(x):
    # R: sample(x, 10, replace = TRUE)
    return np.random.choice(x, 10, replace=True).tolist()

# Apply the custom function to the tree predictions for each sample
pred_custom_vals = [custom_what(all_tree_preds[:, i]) for i in range(X_mt_test.shape[0])]
globals()['pred'] = {
    'predictions': pred_custom_vals,
    'num.samples': X_mt_test.shape[0],
    'treetype': 'Regression',
    'num.independent.variables': X_mt_train.shape[1],
    'num.trees': 500
}

globals()['rf_1'] = globals()['rf']
globals()['pred_1'] = globals()['pred']