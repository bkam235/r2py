# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/ModelMetrics__rd_example__ppv_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__ppv_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import precision_score

# Load data (testDF is a standard dataset in ModelMetrics; creating equivalent structure)
# Since testDF is internal to ModelMetrics, we simulate the loading process
# r2py:entity:data
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=100, n_features=10, random_state=42)
testDF['y'] = y

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
# Setup design matrix (add constant for intercept)
X_glm = sm.add_constant(testDF.drop('y', axis=1))
y_glm = testDF['y']
glmModel = sm.Logit(y_glm, X_glm).fit(disp=0)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X_glm)

# ppv(testDF$y, Preds, cutoff = 0)
# Positive Predictive Value (PPV) is equivalent to precision. 
# With cutoff=0, any prediction > 0 is considered positive.
# r2py:entity:ppv
preds_binary_ppv = (Preds > 0).astype(int)
ppv_val = precision_score(testDF['y'], preds_binary_ppv)
print(ppv_val)

# precision(testDF$y, Preds, cutoff = 0)
# r2py:entity:precision
preds_binary_prec = (Preds > 0).astype(int)
precision_val = precision_score(testDF['y'], preds_binary_prec)
print(precision_val)