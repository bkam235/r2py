import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix
import warnings

# Suppress sklearn warnings for consistency
warnings.filterwarnings("ignore", category=UserWarning)

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__predict_ranger_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mtcars', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Convert shim data to DataFrames
iris = pd.DataFrame(iris)
mtcars = pd.DataFrame(mtcars)

# Classification forest
# r2py:entity:ranger
X_full = iris.drop('Species', axis=1)
y_full = iris['Species']
# ranger default num.trees is 500
rf_full = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=42)
rf_full.fit(X_full, y_full)

# R's ranger summary output
oob_err = (1 - rf_full.oob_score_) * 100
print("      Ranger result\n")
print("Call:\n ranger(Species ~ ., data = iris) \n")
print("Type:                             Classification ")
print(f"Number of trees:                  {rf_full.n_estimators} ")
print(f"Sample size:                      {len(iris)} ")
print(f"Number of independent variables:  {X_full.shape[1]} ")
print(f"Mtry:                             {int(np.sqrt(X_full.shape[1]))} ")
print("Target node size:                 1 ")
print("Variable importance mode:         none ")
print("Splitrule:                        gini ")
print(f"OOB prediction error:             {oob_err:.2f} %")

# train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
# r2py:entity:train.idx
train_idx_r = np.array(globals().get('train.idx', []))

# iris.train <- iris[train.idx, ]
# r2py:entity:iris.train
globals()['iris.train'] = iris.iloc[train_idx_r - 1].reset_index(drop=True)
# iris.test <- iris[-train.idx, ]
# r2py:entity:iris.test
globals()['iris.test'] = iris.drop(iris.index[train_idx_r - 1]).reset_index(drop=True)

# rg.iris <- ranger(Species ~ ., data = iris.train)
# r2py:entity:rg.iris
X_train_iris = globals()['iris.train'].drop('Species', axis=1)
y_train_iris = globals()['iris.train']['Species']
rg_iris = RandomForestClassifier(n_estimators=500, random_state=42)
rg_iris.fit(X_train_iris, y_train_iris)

globals()['rg.iris'] = {
    'predictions': rg_iris.predict(X_train_iris).tolist(),
    'treetype': 'Classification',
    'num.trees': 500,
    'num.samples': len(X_train_iris),
    'num.independent.variables': X_train_iris.shape[1],
    'mtry': int(np.sqrt(X_train_iris.shape[1])),
    'min.node.size': 1,
    'replace': True,
    'splitrule': 'gini',
    'importance.mode': 'none',
    'prediction.error': (1 - rg_iris.score(X_train_iris, y_train_iris)) * 100,
    'dependent.variable.name': 'Species',
    'call': 'ranger(Species ~ ., data = iris.train)',
}

# pred.iris <- predict(rg.iris, data = iris.test)
# r2py:entity:pred.iris
X_test_iris = globals()['iris.test'].drop('Species', axis=1)
pred_iris_vals = rg_iris.predict(X_test_iris)
globals()['pred.iris'] = {
    'predictions': pred_iris_vals.tolist(),
    'num.samples': len(X_test_iris),
    'num.trees': 500,
    'num.independent.variables': X_test_iris.shape[1],
    'treetype': 'Classification'
}

# table(iris.test$Species, pred.iris$predictions)
# r2py:entity:table
labels = ['setosa', 'versicolor', 'virginica']
conf_matrix = confusion_matrix(globals()['iris.test']['Species'], globals()['pred.iris']['predictions'], labels=labels)
print("      " + " ".join(labels))
for i, label in enumerate(labels):
    row_vals = " ".join(f"{val:>10}" for val in conf_matrix[i])
    print(f"  {label:<12} {row_vals}")

# Quantile regression forest
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# r2py:entity:rf
mtcars_train = mtcars.iloc[0:26]
X_train_mt = mtcars_train.drop('mpg', axis=1)
y_train_mt = mtcars_train['mpg']
rf = RandomForestRegressor(n_estimators=500, random_state=42)
rf.fit(X_train_mt, y_train_mt)
globals()['rf'] = rf

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", quantiles = c(0.1, 0.5, 0.9))
# r2py:entity:pred
mtcars_test = mtcars.iloc[26:32]
X_test_mt = mtcars_test.drop('mpg', axis=1)
# Compute quantiles across all trees
tree_preds = np.array([tree.predict(X_test_mt) for tree in rf.estimators_])
quantiles_vals = np.percentile(tree_preds, [10, 50, 90], axis=0).T
globals()['pred'] = {
    'predictions': quantiles_vals.tolist(),
    'num.samples': len(X_test_mt),
    'treetype': 'Regression',
    'num.independent.variables': X_test_mt.shape[1],
    'num.trees': 500
}

print("      quantile= 0.1 quantile= 0.5 quantile= 0.9")
for i, row in enumerate(quantiles_vals):
    print(f"[{i+1},] {row[0]:14.2f} {row[1]:14.2f} {row[2]:14.2f}")

# Quantile regression forest with user-specified function
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
# r2py:entity:rf_1
globals()['rf_1'] = rf

# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", what = function(x) sample(x, 10, replace = TRUE))
# r2py:entity:pred_1
def what_func(x):
    return np.random.choice(x, 10, replace=True).tolist()

# For each observation, get the distribution of predictions from all trees and sample 10
sampled_preds = [what_func(tree_preds[:, i]) for i in range(X_test_mt.shape[0])]
globals()['pred_1'] = {
    'predictions': sampled_preds,
    'num.samples': len(X_test_mt),
    'treetype': 'Regression',
    'num.independent.variables': X_test_mt.shape[1],
    'num.trees': 500
}