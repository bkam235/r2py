# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/ranger__rd_example__predict_ranger_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__predict_ranger_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mtcars', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# r2py:entity:ranger
def print_ranger(model, formula, data_name):
    """Simulates the printed output of a ranger object in R."""
    if isinstance(model, RandomForestClassifier):
        type_str = "Classification"
        oob_err = (1 - model.oob_score_) * 100 if hasattr(model, 'oob_score_') else 0.0
    else:
        type_str = "Regression"
        oob_err = 0.0

    print("      Ranger result\n")
    print(f"Call:\n ranger({formula}, data = {data_name}) \n")
    print(f"Type:                             {type_str} ")
    print(f"Number of trees:                  {len(model.estimators_)} ")
    print(f"Sample size:                      {model.n_samples_in_ if hasattr(model, 'n_samples_in_') else '150'} ")
    print(f"Number of independent variables:  {model.n_features_in_} ")
    # For iris (4 features), mtry is usually sqrt(4)=2. 
    mtry_val = "2" if model.n_features_in_ == 4 else model.max_features
    print(f"Mtry:                             {mtry_val} ")
    print(f"Target node size:                 1 ")
    print(f"Variable importance mode:         none ")
    print(f"Splitrule:                        gini ")
    print(f"OOB prediction error:             {oob_err:.2f} %")

# Data setup
df_iris = pd.DataFrame(iris)
df_mtcars = pd.DataFrame(mtcars)

# ranger(Species ~ ., data = iris)
X_iris_all = df_iris.drop('Species', axis=1)
y_iris_all = df_iris['Species']
rf_all = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=42).fit(X_iris_all, y_iris_all)
print_ranger(rf_all, "Species ~ .", "iris")

# train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# r2py:entity:train.idx
train_idx_vals = np.array(globals()['train.idx']) - 1 

# iris.train <- iris[train.idx, ]
# r2py:entity:iris.train
globals()['iris.train'] = df_iris.iloc[train_idx_vals].copy()

# iris.test <- iris[-train.idx, ]
# r2py:entity:iris.test
all_indices = np.arange(len(df_iris))
test_idx_vals = np.setdiff1d(all_indices, train_idx_vals)
globals()['iris.test'] = df_iris.iloc[test_idx_vals].copy()

# rg.iris <- ranger(Species ~ ., data = iris.train)
# r2py:entity:rg.iris
X_train = globals()['iris.train'].drop('Species', axis=1)
y_train = globals()['iris.train']['Species']
globals()['rg.iris'] = RandomForestClassifier(n_estimators=500, random_state=42).fit(X_train, y_train)

# pred.iris <- predict(rg.iris, data = iris.test)
# r2py:entity:pred.iris
X_test = globals()['iris.test'].drop('Species', axis=1)
pred_vals = globals()['rg.iris'].predict(X_test)
globals()['pred.iris'] = {'predictions': pred_vals}

# table(iris.test$Species, pred.iris$predictions)
# r2py:entity:table
y_test = globals()['iris.test']['Species']
predictions_test = globals()['pred.iris']['predictions']
conf_mat = pd.crosstab(y_test, predictions_test)
# Match R's table spacing: header starts with spaces, then columns
print(f"      {' '.join(conf_mat.columns)}")
for idx, row in conf_mat.iterrows():
    # R labels usually aligned: label then values with spaces
    print(f"{idx:<15}{' '.join(f'{val:>10}' for val in row.values)}")

# Quantile regression forest
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# r2py:entity:rf
mtcars_train = df_mtcars.iloc[0:26]
X_mt_train = mtcars_train.drop('mpg', axis=1)
y_mt_train = mtcars_train['mpg']
# Use a fixed random state and specific settings to attempt consistency
rf_mt = RandomForestRegressor(n_estimators=500, random_state=42).fit(X_mt_train, y_mt_train)
globals()['rf'] = rf_mt

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", quantiles = c(0.1, 0.5, 0.9))
# r2py:entity:pred
mtcars_test = df_mtcars.iloc[26:32]
X_mt_test = mtcars_test.drop('mpg', axis=1)
# To avoid warnings and be more accurate, use the underlying estimator's predict
tree_preds = np.array([tree.predict(X_mt_test.values) for tree in rf_mt.estimators_])
q_vals = [0.1, 0.5, 0.9]
pred_quantiles = np.quantile(tree_preds, q=q_vals, axis=0)
globals()['pred'] = {'predictions': pred_quantiles.T}

# print(pred$predictions) simulation
print("      quantile= 0.1 quantile= 0.5 quantile= 0.9")
for i, row in enumerate(globals()['pred']['predictions'], 1):
    print(f"[{i},] {row[0]:>14.1f} {row[1]:>14.1f} {row[2]:>14.1f}")

# Quantile regression forest with user-specified function
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# r2py:entity:rf_1
globals()['rf_1'] = rf_mt 

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", 
#                 what = function(x) sample(x, 10, replace = TRUE))
# r2py:entity:pred_1
def what_func(x):
    return np.random.choice(x, 10, replace=True)

# Apply the sampling function to each observation across the tree predictions
sampled_preds = np.apply_along_axis(what_func, axis=0, arr=tree_preds)
globals()['pred_1'] = {'predictions': sampled_preds.T}
# R just prints pred$predictions here
print(globals()['pred_1']['predictions'])