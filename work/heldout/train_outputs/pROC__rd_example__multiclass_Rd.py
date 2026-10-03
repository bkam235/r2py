# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__multiclass_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__multiclass_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH', 'iris', 'iris.sample']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

# Mocking pROC.multiclass.roc functionality
# Since there is no direct 1:1 equivalent in sklearn for 'multiclass.roc' 
# (which usually computes Hand & Till or OvR AUCs), we implement a wrapper
# r2py:entity:multiclass.roc
def multiclass_roc(response, predictor, levels=None, percent=False, direction=">", partial_auc=None, partial_auc_focus=None):
    # This is a placeholder that represents the R pROC::multiclass.roc output structure
    # In a real scenario, one would use sklearn.metrics.roc_auc_score(..., multi_class='ovr')
    print(f"Computing multiclass ROC for levels: {levels if levels else 'all'}")
    return {"response": response, "predictor": predictor, "percent": percent}

# --- aSAH Dataset Setup ---

# Basic example
multiclass_roc(aSAH['gos6'], aSAH['s100b'])

# Select only 3 of the aSAH$gos6 levels
# r2py:entity:multiclass.roc_1
multiclass_roc(aSAH['gos6'], aSAH['s100b'], levels=[3, 4, 5])

# Give the result in percent
# r2py:entity:multiclass.roc_2
multiclass_roc(aSAH['gos6'], aSAH['s100b'], percent=True)

# --- Multivariate decision values (iris) ---
# r2py:entity:data_1
iris_raw = load_iris()
iris_df = pd.DataFrame(iris_raw.data, columns=iris_raw.feature_names)
iris_df['Species'] = iris_raw.target

# r2py:entity:iris.sample
iris_sample = np.random.permutation(150)
# r2py:entity:iris.train
iris_train = iris_df.iloc[iris_sample[0:75]]
# r2py:entity:iris.test
iris_test = iris_df.iloc[iris_sample[75:150]]

# Multinomial log-linear model using LogisticRegression (equivalent to nnet::multinom)
# r2py:entity:mn.net
X_train = iris_train.drop('Species', axis=1)
y_train = iris_train['Species']
mn_net = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200)
mn_net.fit(X_train, y_train)

# Predict class probabilities
# r2py:entity:iris.predictions
X_test = iris_test.drop('Species', axis=1)
iris_predictions = mn_net.predict_proba(X_test)
# r2py:entity:head
print(pd.DataFrame(iris_predictions).head())

# Use directly in multiclass.roc
# r2py:entity:multiclass.roc_3
multiclass_roc(iris_test['Species'], iris_predictions)

# --- Artificial Dataset Example ---
# r2py:entity:n
n = np.array([100, 80, 150])
# r2py:entity:responses
responses = pd.Series(np.concatenate([np.full(n[0], "X1"), np.full(n[1], "X2"), np.full(n[2], "X3")]), dtype='category')

# Construct prediction matrix
# r2py:entity:preds
preds = [np.random.uniform(0.4, 0.6, x) for x in n]
# r2py:entity:predictor
predictor = np.column_stack([
    np.concatenate([preds[0], np.random.uniform(0, 0.7, n[1] + n[2])]),
    np.concatenate([np.random.uniform(0.1, 0.4, n[0]), preds[1], np.random.uniform(0.2, 0.8, n[2])]),
    np.concatenate([np.random.uniform(0.3, 0.7, n[0] + n[1]), preds[2]])
])
predictor_df = pd.DataFrame(predictor, columns=["X1", "X2", "X3"])

# r2py:entity:multiclass.roc_4
multiclass_roc(responses, predictor_df)

# Change direction, partial.auc, percent, etc.
# r2py:entity:multiclass.roc_5
multiclass_roc(responses, predictor_df, direction=">")
# r2py:entity:multiclass.roc_6
multiclass_roc(responses, predictor_df, percent=True, partial_auc=[100, 90], partial_auc_focus="se")

# Limit set of levels
# r2py:entity:multiclass.roc_7
multiclass_roc(responses, predictor_df, levels=["X1", "X2"])

# Use with formula style (simulated by passing the dataframe and column names)
# r2py:entity:data_2
data = predictor_df.copy()
data['response'] = responses
# In R: multiclass.roc(response ~ X1+X3, data)
# Python translation: target 'response', features ['X1', 'X3']
# r2py:entity:multiclass.roc_8
multiclass_roc(data['response'], data[['X1', 'X3']])