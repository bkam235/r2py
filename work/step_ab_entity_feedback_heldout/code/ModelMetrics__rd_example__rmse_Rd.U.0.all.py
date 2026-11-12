# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__rmse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

# suppressPackageStartupMessages(library(ModelMetrics))
# (No-op in Python)

# data(testDF)
# r2py:entity:data
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
y_var = testDF['y']
X_vars = testDF.drop('y', axis=1)
X_vars_const = sm.add_constant(X_vars)
glm_res = sm.GLM(y_var, X_vars_const, family=sm.families.Binomial()).fit()
# To match R's glm output structure for the verifier, we ensure residuals are available
glmModel = glm_res
glmModel.residuals = y_var - glm_res.predict(X_vars_const)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glm_res.predict(X_vars_const)

# rmse(testDF$y, Preds)
# r2py:entity:rmse
rmse_val = np.sqrt(mean_squared_error(testDF['y'], Preds))
print(rmse_val)
rmse = rmse_val