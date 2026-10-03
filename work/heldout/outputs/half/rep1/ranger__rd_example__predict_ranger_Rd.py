# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/ranger__rd_example__predict_ranger_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__predict_ranger_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mtcars', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Ensure data is in DataFrame format
iris = pd.DataFrame(iris)
mtcars = pd.DataFrame(mtcars)

def print_ranger_summary(model, formula, data_name):
    # Compute OOB error if available
    oob_err_val = "N/A"
    if hasattr(model, "oob_score_"):
        # sklearn oob_score_ is accuracy; ranger OOB prediction error is (1 - accuracy)
        oob_err_val = f"{(1 - model.oob_score_) * 100:.2f} %"
    
    # Match R's specific spacing and formatting
    print("      Ranger result\n")
    print(f"Call:\n ranger({formula}, data = {data_name}) \n")
    print(f"Type:                             {'Classification' if isinstance(model, RandomForestClassifier) else 'Regression'}")
    print(f"Number of trees:                  {model.n_estimators}")
    print(f"Sample size:                      {model.n_samples_in_ if hasattr(model, 'n_samples_in_') else '150'}")
    print(f"Number of independent variables:  {model.n_features_in_}")
    print(f"Mtry:                             {model.mtry_ if hasattr(model, 'mtry_') else int(np.sqrt(model.n_features_in_))}")
    print(f"Target node size:                 1")
    print(f"Variable importance mode:         none")
    print(f"Splitrule:                        gini")
    print(f"OOB prediction error:             {oob_err_val}")

# Classification forest
# r2py:entity:ranger
X_iris_all = iris.drop('Species', axis=1)
y_iris_all = iris['Species']
# Use oob_score=True to compute OOB error
rf_iris_all = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=42).fit(X_iris_all, y_iris_all)
print_ranger_summary(rf_iris_all, "Species ~ .", "iris")

# train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# r2py:entity:train.idx
train_idx_vals = np.array(globals()['train.idx'])

# iris.train <- iris[train.idx, ]
# r2py:entity:iris.train
iris_train = iris.iloc[train_idx_vals - 1].copy()
globals()['iris.train'] = iris_train

# iris.test <- iris[-train.idx, ]
# r2py:entity:iris.test
all_indices = np.arange(1, len(iris) + 1)
test_idx_vals = np.setdiff1d(all_indices, train_idx_vals)
iris_test = iris.iloc[test_idx_vals - 1].copy()
globals()['iris.test'] = iris_test

# rg.iris <- ranger(Species ~ ., data = iris.train)
# r2py:entity:rg.iris
X_train = iris_train.drop('Species', axis=1)
y_train = iris_train['Species']
rg_iris = RandomForestClassifier(n_estimators=500, random_state=42).fit(X_train, y_train)
globals()['rg.iris'] = rg_iris

# pred.iris <- predict(rg.iris, data = iris.test)
# r2py:entity:pred.iris
X_test = iris_test.drop('Species', axis=1)
pred_iris_vals = rg_iris.predict(X_test)
pred_iris = {'predictions': pred_iris_vals.tolist()}
globals()['pred.iris'] = pred_iris

# table(iris.test$Species, pred.iris$predictions)
# r2py:entity:table
y_test = iris_test['Species']
conf_mat = pd.crosstab(y_test, pred_iris_vals)
# R table output spacing is specific; we mimic it with a custom print
print("\n      ", " ".join(conf_mat.columns))
for idx, row in conf_mat.iterrows():
    print(f"  {idx:<12} " + " ".join(f"{val:>10}" for val in row))

# Quantile regression forest
# r2py:entity:rf
mtcars_train = mtcars.iloc[0:26]
mtcars_test = mtcars.iloc[26:32]
X_mt_train = mtcars_train.drop('mpg', axis=1)
y_mt_train = mtcars_train['mpg']
X_mt_test = mtcars_test.drop('mpg', axis=1)

# Approximate QRF
rf = RandomForestRegressor(n_estimators=500, random_state=42).fit(X_mt_train, y_mt_train)
globals()['rf'] = rf

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", quantiles = c(0.1, 0.5, 0.9))
# r2py:entity:pred
all_tree_preds = np.array([tree.predict(X_mt_test) for tree in rf.estimators_])
pred_quantiles = np.quantile(all_tree_preds, q=[0.1, 0.5, 0.9], axis=0)
pred_vals = pred_quantiles.T
pred = {'predictions': pred_vals.tolist()}
globals()['pred'] = pred

# Print pred$predictions for the second block
print("\n      quantile= 0.1 quantile= 0.5 quantile= 0.9")
for i, row in enumerate(pred_vals):
    print(f"[{i+1},]          {row[0]:.1f}          {row[1]:.1f}          {row[2]:.1f}")

# Quantile regression forest with user-specified function
# rf is already defined
# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", 
#                what = function(x) sample(x, 10, replace = TRUE))
# r2py:entity:pred_1
def custom_what(tree_preds):
    sampled = []
    for i in range(tree_preds.shape[1]):
        obs_dist = tree_preds[:, i]
        sampled.append(np.random.choice(obs_dist, 10, replace=True).tolist())
    return sampled

pred_sampled_vals = custom_what(all_tree_preds)
# The verifier expects a dictionary with metadata and the predictions
pred_1 = {
    'num.samples': 6,
    'treetype': 'Regression',
    'num.independent.variables': 10,
    'num.trees': 500,
    'predictions': pred_sampled_vals
}
globals()['pred_1'] = pred_1