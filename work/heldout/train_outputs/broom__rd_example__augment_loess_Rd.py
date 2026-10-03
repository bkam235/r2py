# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_loess_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_loess_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Convert mtcars to DataFrame if it's a dict
if isinstance(mtcars, dict):
    mtcars = pd.DataFrame(mtcars)

# r2py:entity:lo
class LoessModel:
    def __init__(self, formula, data, control=None):
        # formula: 'mpg ~ hp + wt'
        self.formula = formula
        self.data = data
        # Parse formula
        parts = formula.split('~')
        self.response = parts[0].strip()
        self.predictors = [p.strip() for p in parts[1].split('+')]
        
        self.X_train = data[self.predictors].values
        self.y_train = data[self.response].values
        self.terms = formula

    def predict(self, newdata=None):
        if newdata is None:
            X = self.X_train
        else:
            X = newdata[self.predictors].values
            
        predictions = []
        for x_val in X:
            # Basic LOESS approximation: Weighted Least Squares with Tricube kernel
            # Calculate distances to all training points
            dists = np.linalg.norm(self.X_train - x_val, axis=1)
            
            # Define bandwidth (span) - simplified as 0.75 of distance to furthest point or fixed
            # In a real loess, this is optimized. Here we use a reasonable heuristic.
            bandwidth = np.percentile(dists, 75)
            if bandwidth == 0: bandwidth = 1e-5
            
            # Tricube weight function
            weights = (1 - (dists / bandwidth)**3)**3
            weights[dists > bandwidth] = 0
            
            if np.sum(weights) == 0:
                predictions.append(np.mean(self.y_train))
            else:
                # WLS
                W = np.diag(weights)
                # Solve (X^T W X) beta = X^T W y
                X_mat = np.column_stack([np.ones(len(self.X_train)), self.X_train])
                try:
                    beta = np.linalg.lstsq(W @ X_mat, W @ self.y_train, rcond=None)[0]
                    pred = np.dot(np.append(1, x_val), beta)
                    predictions.append(pred)
                except:
                    predictions.append(np.mean(self.y_train))
                    
        return np.array(predictions)

# r2py:entity:augment
def augment(x, data=None, newdata=None):
    # Mimic broom::augment.loess logic
    if newdata is not None:
        df = newdata.copy()
        fitted = x.predict(newdata=newdata)
    elif data is not None:
        df = data.copy()
        fitted = x.predict(newdata=data)
    else:
        df = x.data.copy()
        fitted = x.predict()
    
    df['.fitted'] = fitted
    
    # Calculate residuals if response variable is present
    if x.response in df.columns:
        df['.resid'] = df[x.response] - df['.fitted']
        
    return df

# lo <- loess(mpg ~ hp + wt, mtcars, control = loess.control(surface = "direct"))
# r2py:entity:lo
lo = LoessModel(formula="mpg ~ hp + wt", data=mtcars)

# augment(lo)
# r2py:entity:augment
res_1 = augment(lo)

# augment(lo, mtcars)
# r2py:entity:augment_1
res_2 = augment(lo, data=mtcars)

# augment(lo, newdata = head(mtcars))
# r2py:entity:augment_2
res_3 = augment(lo, newdata=mtcars.head())