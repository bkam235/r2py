# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__logLoss_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end
# r2py:data_shim managed by the harness (loads R's input data) - do not write it

import pandas as pd
import numpy as np
import statsmodels.api as sm
# r2py:entity:logLoss
from sklearn.metrics import log_loss


def _r_print_scalar(v):
    # Mimic R's default print for a length-1 numeric: 7 significant digits
    print("[1] " + format(float(v), ".7g"))


# r2py:entity:data
# data(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop('y', axis=1)
X_with_intercept = sm.add_constant(X)
glmModel = sm.GLM(y, X_with_intercept, family=sm.families.Binomial()).fit()

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X_with_intercept)

# logLoss(testDF$y, Preds)
_logLoss = log_loss


def ml_log_loss(actual, predicted):
    predicted = np.maximum(np.minimum(predicted, 1 - 1e-15), 1e-15)
    return _logLoss(actual, predicted)


# r2py:entity:logLoss
logLoss_val = ml_log_loss(testDF['y'].to_numpy(), Preds)
_r_print_scalar(logLoss_val)

# logLoss(glmModel)
# r2py:entity:logLoss_1
logLoss_glm_val = ml_log_loss(y.to_numpy(), glmModel.mu)
_r_print_scalar(logLoss_glm_val)