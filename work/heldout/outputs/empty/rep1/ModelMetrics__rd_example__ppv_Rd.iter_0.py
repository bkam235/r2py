# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/ModelMetrics__rd_example__ppv_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__ppv_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import precision_score

# Mocking testDF as it is a built-in dataset in ModelMetrics
# In a real scenario, you would load your actual data here
# r2py:entity:data
from sklearn.datasets import make_classification
X_raw, y_raw = make_classification(n_samples=100, n_features=5, random_state=42)
testDF['y'] = y_raw

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop('y', axis=1)
X = sm.add_constant(X) # Add intercept to match R's glm behavior
glmModel = sm.Logit(y, X).fit(disp=0)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X)

# ppv(testDF$y, Preds, cutoff = 0)
# ppv (Positive Predictive Value) is equivalent to precision
# Since cutoff=0 in R's ModelMetrics often implies using the probabilities 
# and applying a threshold, but specifically for precision_score, 
# we must binarize the predictions.
# r2py:entity:ppv
binary_preds = (Preds > 0).astype(int) 
ppv_val = precision_score(testDF['y'], binary_preds)
print(ppv_val)

# precision(testDF$y, Preds, cutoff = 0)
# r2py:entity:precision
precision_val = precision_score(testDF['y'], binary_preds)
print(precision_val)