# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ranger__rd_example__predict_ranger_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'mtcars', 'train.idx']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import warnings

# Suppress sklearn warnings about feature names
warnings.filterwarnings("ignore", category=UserWarning)

# Convert shimmed data
iris = pd.DataFrame(iris)
mtcars = pd.DataFrame(mtcars)
train_idx = globals().get('train.idx')

# r2py:entity:ranger
def ranger_summary_print(model_obj, formula, data_name):
    """Prints a summary simulating R's ranger object print method."""
    print("      Ranger result\n")
    print(f"Call:\n ranger({formula}, data = {data_name}) \n")
    print(f"Type:                             {model_obj['treetype']} ")
    print(f"Number of trees:                  {model_obj['num.trees']} ")
    print(f"Sample size:                      {model_obj['num.samples']} ")
    print(f"Number of independent variables:  {model_obj['num.independent.variables']} ")
    print(f"Mtry:                             {model_obj.get('mtry', '2')} ")
    print(f"Target node size:                 {model_obj.get('node_size', '1')} ")
    print(f"Variable importance mode:         none ")
    print(f"Splitrule:                        gini ")
    # OOB error is calculated by sklearn's oob_score_
    oob_err = 100 * (1 - model_obj['oob_score']) if 'oob_score' in model_obj else 4.00
    print(f"OOB prediction error:             {oob_err:.2f} %")

# Classification forest
# ranger(Species ~ ., data = iris)
X_all_iris = iris.drop('Species', axis=1)
y_all_iris = iris['Species']
rf_iris_all_model = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=42)
rf_iris_all_model.fit(X_all_iris, y_all_iris)

ranger_res_all = {
    'treetype': 'Classification',
    'num.trees': 500,
    'num.samples': len(iris),
    'num.independent.variables': X_all_iris.shape[1],
    'oob_score': rf_iris_all_model.oob_score_
}
ranger_summary_print(ranger_res_all, "Species ~ .", "iris")

# train.idx is 1-indexed from R
# r2py:entity:train.idx
train_indices_py = [i - 1 for i in train_idx]
# r2py:entity:iris.train
globals()['iris.train'] = iris.iloc[train_indices_py].copy()
# r2py:entity:iris.test
globals()['iris.test'] = iris.drop(iris.index[train_indices_py]).copy()

iris_train = globals()['iris.train']
iris_test = globals()['iris.test']

# r2py:entity:rg.iris
# rg.iris <- ranger(Species ~ ., data = iris.train)
X_train_iris = iris_train.drop('Species', axis=1)
y_train_iris = iris_train['Species']
rg_iris_model = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=42)
rg_iris_model.fit(X_train_iris, y_train_iris)

globals()['rg.iris'] = {
    'predictions': rg_iris_model.predict(X_train_iris).tolist(),
    'treetype': 'Classification',
    'num.trees': 500,
    'num.samples': len(iris_train),
    'num.independent.variables': X_train_iris.shape[1],
    'oob_score': rg_iris_model.oob_score_
}

# r2py:entity:pred.iris
# pred.iris <- predict(rg.iris, data = iris.test)
X_test_iris = iris_test.drop('Species', axis=1)
pred_iris_vals = rg_iris_model.predict(X_test_iris)
globals()['pred.iris'] = {
    'predictions': pred_iris_vals.tolist()
}

# r2py:entity:table
# table(iris.test$Species, pred.iris$predictions)
conf_matrix = pd.crosstab(iris_test['Species'], globals()['pred.iris']['predictions'])
# Precise R-like table formatting
col_names = " ".join(conf_matrix.columns)
print(f"      {col_names}")
for idx, row in conf_matrix.iterrows():
    row_vals = "          ".join(map(str, row.values))
    print(f"  {idx:<12} {row_vals}")

# Quantile regression forest
# r2py:entity:rf
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
X_train_mt = mtcars.iloc[0:26].drop('mpg', axis=1)
y_train_mt = mtcars.iloc[0:26]['mpg']
rf_model = RandomForestRegressor(n_estimators=500, oob_score=True, random_state=42)
rf_model.fit(X_train_mt, y_train_mt)

globals()['rf'] = {
    'model': rf_model,
    'treetype': 'Regression',
    'num.trees': 500,
    'num.samples': 26,
    'num.independent.variables': X_train_mt.shape[1],
    'oob_score': rf_model.oob_score_
}

# r2py:entity:pred
# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", quantiles = c(0.1, 0.5, 0.9))
X_test_mt = mtcars.iloc[26:32].drop('mpg', axis=1)
all_tree_preds = np.array([tree.predict(X_test_mt) for tree in rf_model.estimators_])
quantiles_vals = np.percentile(all_tree_preds, [10, 50, 90], axis=0).T
globals()['pred'] = {'predictions': quantiles_vals.tolist()}

# Print pred$predictions
print("      quantile= 0.1 quantile= 0.5 quantile= 0.9")
for i, row in enumerate(globals()['pred']['predictions'], 1):
    print(f"[{i},]          {row[0]:.1f}          {row[1]:.1f}          {row[2]:.1f}")

# Quantile regression forest with user-specified function
# r2py:entity:rf_1
# rf <- ranger(mpg ~ ., mtcars[1:26, ], quantreg = TRUE)
rf_model_1 = RandomForestRegressor(n_estimators=500, oob_score=True, random_state=42)
rf_model_1.fit(X_train_mt, y_train_mt)
globals()['rf'] = {
    'model': rf_model_1,
    'treetype': 'Regression',
    'num.trees': 500,
    'num.samples': 26,
    'num.independent.variables': X_train_mt.shape[1],
    'oob_score': rf_model_1.oob_score_
}

# r2py:entity:pred_1
# pred <- predict(rf, mtcars[27:32, ], type = "quantiles", 
#                 what = function(x) sample(x, 10, replace = TRUE))
all_tree_preds_1 = np.array([tree.predict(X_test_mt) for tree in rf_model_1.estimators_])
sampled_preds = []
for i in range(X_test_mt.shape[0]):
    sample_res = np.random.choice(all_tree_preds_1[:, i], 10, replace=True)
    sampled_preds.append(sample_res)

globals()['pred'] = {
    'predictions': np.array(sampled_preds).tolist(),
    'num.samples': X_test_mt.shape[0],
    'treetype': 'Regression',
    'num.independent.variables': X_test_mt.shape[1],
    'num.trees': 500
}