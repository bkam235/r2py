# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ModelMetrics__rd_example__tnr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['testDF']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm

# r2py:entity:data
testDF = pd.DataFrame(testDF)

# glmModel <- glm(y ~ ., data = testDF, family="binomial")
# r2py:entity:glmModel
y = testDF['y']
X = testDF.drop('y', axis=1)
X_with_const = sm.add_constant(X)
# R's glm(family="binomial") is a logistic regression.
glmModel = sm.Logit(y, X_with_const).fit(disp=0)

# Preds <- predict(glmModel, type = 'response')
# r2py:entity:Preds
Preds = glmModel.predict(X_with_const).values

# r2py:entity:tnr
def calculate_tnr(actual, predicted, cutoff=0.5):
    # Predicted is 1 if predicted >= cutoff, else 0
    y_pred = (predicted >= cutoff).astype(int)
    actual = np.array(actual)
    
    # True Negatives: actual == 0 and predicted == 0
    tn = np.sum((actual == 0) & (y_pred == 0))
    # False Positives: actual == 0 and predicted == 1
    fp = np.sum((actual == 0) & (y_pred == 1))
    
    if (tn + fp) == 0:
        return np.nan
    return tn / (tn + fp)

# tnr(testDF$y, Preds, cutoff = 0)
tnr_val = calculate_tnr(testDF['y'], Preds, cutoff=0)
# R prints 0 for 0.0 in this specific case
print(f"[1] {int(tnr_val) if tnr_val == 0 else tnr_val}")

# specificity(testDF$y, Preds, cutoff = 0)
# r2py:entity:specificity
spec_val = calculate_tnr(testDF['y'], Preds, cutoff=0)
print(f"[1] {int(spec_val) if spec_val == 0 else spec_val}")