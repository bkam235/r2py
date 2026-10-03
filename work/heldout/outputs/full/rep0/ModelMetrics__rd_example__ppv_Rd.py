# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:entity:data
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

# Ensure testDF is a DataFrame
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop(columns=['y'])
X = sm.add_constant(X)
glmModel = sm.Logit(y, X).fit(disp=0)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X).values

# r2py:entity:ppv
def calculate_ppv(actual, predicted, cutoff=0.5):
    # In ModelMetrics, ppv/precision: predicted >= cutoff is positive.
    # If cutoff is 0, all predictions (which are [0, 1]) are >= 0.
    binary_preds = (predicted >= cutoff).astype(int)
    return precision_score(actual, binary_preds, zero_division=0)

# ppv(testDF$y, Preds, cutoff = 0)
ppv = calculate_ppv(y, Preds, cutoff=0)

# precision(testDF$y, Preds, cutoff = 0)
# r2py:entity:precision
precision = calculate_ppv(y, Preds, cutoff=0)