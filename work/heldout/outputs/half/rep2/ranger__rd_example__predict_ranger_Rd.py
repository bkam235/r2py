# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/ranger__rd_example__predict_ranger_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__predict_ranger_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mtcars', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score

# Convert shim data to DataFrames
iris = pd.DataFrame(iris)
mtcars = pd.DataFrame(mtcars)

def print_ranger_result(model, X, y, formula_str):
    p = X.shape[1]
    mtry = int(np.sqrt(p))
    
    if hasattr(model, 'oob_score_'):
        oob_err = (1 - model.oob_score_) * 100
    else:
        preds = model.predict(X)
        oob_err = (1 - accuracy_score(y, preds)) * 100

    print("      Ranger result\n")
    print(f"Call:\n ranger({formula_str}) \n")
    print(f"Type:                             {'Classification ' if isinstance(model, RandomForestClassifier) else 'Regression '}")
    print(f"Number of trees:                  {model.n_estimators} ")
    print(f"Sample size:                      {X.shape[0]} ")
    print(f"Number of independent variables:  {X.shape[1]} ")
    print(f"Mtry:                             {mtry} ")
    print(f"Target node size:                 1 ")
    print(f"Variable importance mode:         none ")
    print(f"Splitrule:                        gini ")
    print(f"OOB prediction error:             {oob_err:.2f} %")

# Classification forest
# ranger(Species ~ ., data = iris)
# r2py:entity:ranger
X_iris_full = iris.drop('Species', axis=1).values
y_iris_full = iris['Species'].values
clf_full = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=0, max_features='sqrt').fit(X_iris_full, y_iris_full)
print_ranger_result(clf_full, X_iris_full, y_iris_full, "Species ~ ., data = iris")

# train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# r2py:entity:train.idx
train_idx_val = np.array(globals().get('train.idx', [])) - 1

# iris.train <- iris[train.idx, ]
# r2py:entity:iris.train
globals()['iris.train'] = iris.iloc[train_idx_val].reset_index(drop=True)
iris_train = globals()['iris.train']

# iris.test <- iris[-train.idx, ]
# r2py:entity:iris.test
globals()['iris.test'] = iris.drop(iris.index[train_idx_val]).reset_index(drop=True)
iris_test = globals()['iris.test']

# rg.iris <- ranger(Species ~ ., data = iris.train)
# r2py:entity:rg.iris
X_train_iris = iris_train.drop('Species', axis=1).values
y_train_iris = iris_train['Species'].values
rg_iris_model = RandomForestClassifier(n_estimators=500, random_state=0, max_features='sqrt').fit(X_train_iris, y_train_iris)
globals()['rg.iris'] = {
    'predictions': rg_iris_model.predict(X_train_iris).tolist(),
    'treetype': 'Classification'
}
rg_iris = globals()['rg.iris']

# pred.iris <- predict(rg.iris, data = iris.test)
# r2py:entity:pred.iris
X_test_iris = iris_test.drop('Species', axis=1).values
pred_iris_vals = rg_iris_model.predict(X_test_iris)
globals()['pred.iris'] = {'predictions': pred_iris_vals.tolist()}
pred_iris = globals()['pred.iris']

# table(iris.test$Species, pred.iris$predictions)
# r2py:entity:table
table_out = pd.crosstab(iris_test['Species'], pred_iris['predictions'])
# R table output format: columns spaced, rows with name then spaced values
print("      " + " ".join(table_out.columns))
for idx, row in table_out.iterrows():
    # R uses variable width; we approximate with 10-char padding
    row_str = " ".join(f"{int(v):>10}" for v in row.values)
    print(f"  {idx:<11}{row_str}")

# Quantile regression forest
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# r2py:entity:rf
mtcars_train = mtcars.iloc[0:26]
mtcars_test = mtcars.iloc[26:32]
X_train_mt = mtcars_train.drop('mpg', axis=1).values
y_train_mt = mtcars_train['mpg'].values
X_test_mt = mtcars_test.drop('mpg', axis=1).values

mtry_reg = int(X_train_mt.shape[1] / 3)
rf_model = RandomForestRegressor(n_estimators=500, random_state=0, max_features=mtry_reg).fit(X_train_mt, y_train_mt)
globals()['rf'] = {
    'treetype': 'Regression', 
    'num.trees': 500, 
    'num.independent.variables': X_train_mt.shape[1],
    'predictions': rf_model.predict(X_train_mt).tolist()
}
rf = globals()['rf']

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", quantiles = c(0.1, 0.5, 0.9))
# r2py:entity:pred
tree_preds_mt = np.array([tree.predict(X_test_mt) for tree in rf_model.estimators_])
pred_quantiles = np.quantile(tree_preds_mt, q=[0.1, 0.5, 0.9], axis=0).T
globals()['pred'] = {'predictions': pred_quantiles.tolist()}
pred = globals()['pred']

print("      quantile= 0.1 quantile= 0.5 quantile= 0.9")
for i, row in enumerate(pred['predictions'], 1):
    formatted_row = " ".join(f"{val:>10.1f}" for val in row)
    print(f"[{i},] {formatted_row}")

# Quantile regression forest with user-specified function
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# r2py:entity:rf_1
rf_1_model = RandomForestRegressor(n_estimators=500, random_state=0, max_features=mtry_reg).fit(X_train_mt, y_train_mt)
globals()['rf'] = {
    'treetype': 'Regression', 
    'num.trees': 500, 
    'num.independent.variables': X_train_mt.shape[1],
    'predictions': rf_1_model.predict(X_train_mt).tolist()
}
rf_1 = globals()['rf']

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", 
#                 what = function(x) sample(x, 10, replace = TRUE))
# r2py:entity:pred_1
def custom_what(x):
    return np.random.choice(x, 10, replace=True).tolist()

tree_preds_mt_1 = np.array([tree.predict(X_test_mt) for tree in rf_1_model.estimators_])
pred_custom_vals = [custom_what(tree_preds_mt_1[:, i]) for i in range(X_test_mt.shape[0])]
globals()['pred'] = {
    'num.samples': len(pred_custom_vals),
    'treetype': 'Regression',
    'num.independent.variables': X_train_mt.shape[1],
    'num.trees': 500,
    'predictions': pred_custom_vals
}
pred_1 = globals()['pred']