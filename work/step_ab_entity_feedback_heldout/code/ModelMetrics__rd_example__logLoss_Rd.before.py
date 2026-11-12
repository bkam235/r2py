# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__logLoss_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
# r2py:entity:logLoss
from sklearn.metrics import log_loss

# data(testDF)
# r2py:entity:data
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# In R, glm(y ~ ., ...) includes an intercept by default.
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop('y', axis=1)
X_with_intercept = sm.add_constant(X)
glmModel = sm.GLM(y, X_with_intercept, family=sm.families.Binomial()).fit()

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X_with_intercept)

# logLoss(testDF$y, Preds)
# ModelMetrics::logLoss for binomial is equivalent to sklearn.metrics.log_loss
# r2py:entity:logLoss
logLoss_val = log_loss(testDF['y'], Preds)

# logLoss(glmModel)
# The S3 method logLoss.glm uses modelObject$y and modelObject$fitted.values
# r2py:entity:logLoss_1
logLoss_glm_val = log_loss(y, glmModel.mu)

# To match R's implicit printing behavior in the script:
print(logLoss_val)
print(logLoss_glm_val)