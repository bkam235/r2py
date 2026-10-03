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

# Convert shim data to DataFrame
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop('y', axis=1)
X = sm.add_constant(X)
glmModel = sm.GLM(y, X, family=sm.families.Binomial()).fit()

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X)

# r2py:entity:ppv
def ppv(actual, predicted, cutoff=0.5):
    """
    Positive Predictive Value (Precision).
    In ModelMetrics, values > cutoff are considered positive.
    """
    actual = np.asarray(actual)
    predicted = np.asarray(predicted)
    
    # In ModelMetrics, predicted > cutoff is the condition for a positive prediction
    pred_binary = (predicted > cutoff).astype(int)
    
    tp = np.sum((actual == 1) & (pred_binary == 1))
    fp = np.sum((actual == 0) & (pred_binary == 1))
    
    if (tp + fp) == 0:
        return np.nan
    return tp / (tp + fp)

# r2py:entity:precision
def precision(actual, predicted, cutoff=0.5):
    return ppv(actual, predicted, cutoff)

# ppv(testDF$y, Preds, cutoff = 0)
# r2py:entity:ppv
res_ppv = ppv(testDF['y'], Preds, cutoff=0)
print(f"[1] {res_ppv:.2f}" if not np.isnan(res_ppv) else "[1] NaN")

# precision(testDF$y, Preds, cutoff = 0)
# r2py:entity:precision
res_precision = precision(testDF['y'], Preds, cutoff=0)
print(f"[1] {res_precision:.2f}" if not np.isnan(res_precision) else "[1] NaN")