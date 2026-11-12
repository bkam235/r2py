# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ModelMetrics__rd_example__gini_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__gini_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# data(testDF)
# r2py:entity:data
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
X = testDF.drop(columns=['y'])
y = testDF['y']
# LogisticRegression(penalty=None) is equivalent to glm with family="binomial" (no regularization)
glmModel = LogisticRegression(penalty=None).fit(X, y)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict_proba(X)[:, 1]

# gini(testDF$y, Preds)
# ModelMetrics::gini is calculated as (2 * AUC) - 1
# r2py:entity:gini
gini_val = 2 * roc_auc_score(y, Preds) - 1

# gini(glmModel)
# The S3 method for glm uses the model's fitted values (predicted probabilities)
# r2py:entity:gini_1
Preds_model = glmModel.predict_proba(X)[:, 1]
gini_model = 2 * roc_auc_score(y, Preds_model) - 1