# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__mse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

# suppressPackageStartupMessages(library(ModelMetrics))
# Translated: Library import handled by imports above

# data(testDF)
# r2py:entity:data
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop('y', axis=1)
X = sm.add_constant(X)
glmModel = sm.Logit(y, X).fit(disp=0)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X)

# mse(testDF$y, Preds)
# r2py:entity:mse
mse = mean_squared_error(testDF['y'], Preds)