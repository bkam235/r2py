# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__auc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score

# suppressPackageStartupMessages(library(ModelMetrics))
# data(testDF) - Loaded via shim

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# R's 'y ~ .' means all other columns.
# r2py:entity:glmModel
all_cols = testDF.columns.tolist()
if 'y' in all_cols:
    all_cols.remove('y')
formula_str = 'y ~ ' + ' + '.join(all_cols)
glmModel = smf.glm(formula=formula_str, data=testDF, family=sm.families.Binomial()).fit()

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(testDF)

# auc(testDF$y, Preds)
# r2py:entity:auc
auc_val = roc_auc_score(testDF['y'], Preds)
print(auc_val)

# auc(glmModel)
# using s3 method for glm
# r2py:entity:auc_1
# The S3 method for glm in ModelMetrics extracts the response and the fitted values.
auc_val_1 = roc_auc_score(testDF['y'], glmModel.predict(testDF))
print(auc_val_1)