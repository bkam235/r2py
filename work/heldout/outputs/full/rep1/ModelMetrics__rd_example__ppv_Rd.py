# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__ppv_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import precision_score

# data(testDF)
# r2py:entity:data
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# In R, y ~ . uses all other columns as predictors
# r2py:entity:glmModel
X_glm = testDF.drop('y', axis=1)
X_glm = sm.add_constant(X_glm)
glmModel = sm.Logit(testDF['y'], X_glm).fit(disp=0)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X_glm)

# ppv(testDF$y, Preds, cutoff = 0)
# ModelMetrics::ppv/precision: predicted = (predicted > cutoff)
# r2py:entity:ppv
preds_binary_ppv = (Preds > 0).astype(int)
ppv = precision_score(testDF['y'], preds_binary_ppv, zero_division=1)

# precision(testDF$y, Preds, cutoff = 0)
# r2py:entity:precision
preds_binary_prec = (Preds > 0).astype(int)
precision = precision_score(testDF['y'], preds_binary_prec, zero_division=1)