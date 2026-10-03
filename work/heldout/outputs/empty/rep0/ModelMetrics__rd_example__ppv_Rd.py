# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/ModelMetrics__rd_example__ppv_Rd.py'
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
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop('y', axis=1)
X_with_const = sm.add_constant(X)
glmModel = sm.Logit(y, X_with_const).fit(disp=0)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X_with_const)

# Define a helper for ppv/precision since R's ModelMetrics uses a threshold
# r2py:entity:ppv
def calculate_precision(actual, predicted, cutoff=0.5):
    # R's ppv/precision: predicted > cutoff is True
    y_pred_binary = (predicted > cutoff).astype(int)
    return precision_score(actual, y_pred_binary, zero_division=0)

# ppv(testDF$y, Preds, cutoff = 0)
# r2py:entity:ppv
ppv_val = calculate_precision(testDF['y'], Preds, cutoff=0)
print(ppv_val)

# precision(testDF$y, Preds, cutoff = 0)
# r2py:entity:precision
precision_val = calculate_precision(testDF['y'], Preds, cutoff=0)
print(precision_val)