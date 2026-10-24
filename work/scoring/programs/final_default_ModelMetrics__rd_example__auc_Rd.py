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
from statsmodels.formula.api import glm
from sklearn.metrics import roc_auc_score
import warnings

# suppressPackageStartupMessages(library(ModelMetrics))
# r2py:entity:suppressPackageStartupMessages
pass

# data(testDF)
# r2py:entity:data
# testDF is already loaded by the shim

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
all_cols = testDF.columns.tolist()
if 'y' in all_cols:
    all_cols.remove('y')
formula_str = 'y ~ ' + ' + '.join(all_cols)

# To prevent the harness crash and provide a structure similar to R's glm output
def fit_model():
    model_fit = glm(formula=formula_str, data=testDF, family=sm.families.Binomial()).fit()
    
    # Extract coefficients and order them as (Intercept), x1, x2...
    params = model_fit.params
    coefs_dict = {}
    if 'Intercept' in params.index:
        coefs_dict['(Intercept)'] = params['Intercept']
    for col in all_cols:
        if col in params.index:
            coefs_dict[col] = params[col]
    
    # Manual calculation of deviance residuals to match R's glm()
    y = testDF['y'].values.astype(float)
    p = model_fit.predict(testDF).values
    p = np.clip(p, 1e-15, 1 - 1e-15)
    
    # Use np.where to avoid 0 * log(0) which results in NaN
    term1 = np.where(y > 0, y * np.log(y / p), 0.0)
    term2 = np.where(y < 1, (1 - y) * np.log((1 - y) / (1 - p)), 0.0)
    
    dev = 2 * (term1 + term2)
    resids = np.sign(y - p) * np.sqrt(np.maximum(dev, 0))
    
    residuals_dict = {str(i+1): val for i, val in enumerate(resids)}
    
    return {
        'coefficients': coefs_dict,
        'residuals': residuals_dict,
        'fitted': model_fit.predict(testDF)
    }

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # r2py:entity:glmModel
    glmModel = fit_model()

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel['fitted']

# auc(testDF$y, Preds)
# r2py:entity:auc
auc_val = roc_auc_score(testDF['y'], Preds)
print(f"[1] {auc_val:.7f}")

# auc(glmModel)
# r2py:entity:auc_1
# R's auc.glm uses model$y and model$fitted.values
auc_val_glm = roc_auc_score(testDF['y'], glmModel['fitted'])
print(f"[1] {auc_val_glm:.7f}")