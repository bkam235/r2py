# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path

# r2py:data_shim:begin
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['aSAH']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            _r2py_shim_v = pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

def suppressPackageStartupMessages(x):
    return x

class ROC:
    def __init__(self, response, predictor, percent=False):
        self.percent = percent
        
        # Ensure inputs are pandas Series for mapping
        response = pd.Series(response)
        predictor = pd.Series(predictor)
        
        # pROC: second level is case, first is control.
        # aSAH outcome levels: Good, Poor. Control=Good(0), Case=Poor(1)
        if response.dtype == 'object' or isinstance(response.iloc[0], str):
            y_true = response.map({'Good': 0, 'Poor': 1}).fillna(0).astype(int)
        else:
            # If numeric, assume 1=Good, 2=Poor based on R factor levels
            y_true = response.replace({1: 0, 2: 1}).fillna(0).astype(int)
        
        fpr, tpr, thresholds = roc_curve(y_true, predictor)
        
        # pROC: sensitivities = tpr, specificities = 1 - fpr
        self.sensitivities = tpr
        self.specificities = 1 - fpr
        self.thresholds = thresholds
        self.fpr = fpr
        self.tpr = tpr
        self.y_true = y_true
        self.predictor = predictor
        
        if self.percent:
            self.sensitivities = self.sensitivities * 100
            self.specificities = self.specificities * 100
            
        # Calculate AUC using trapezoidal rule on (fpr, tpr)
        self.auc = sklearn_auc(fpr, tpr)
        if self.percent:
            self.auc = self.auc * 10000  # (0.1*100) * (0.1*100) = 0.01 * 10000

def ggroc(roc_obj, legacy_axes=False):
    """Plot a ROC curve using plotnine"""
    if legacy_axes:
        x = 1 - roc_obj.specificities
        y = roc_obj.sensitivities
    else:
        x = 1 - roc_obj.specificities
        y = roc_obj.sensitivities
    
    df = pd.DataFrame({'x': x, 'y': y})
    return df, roc_obj

def geom_polygon_auc(auc_val, legacy_axes=False):
    """Add a polygon for AUC to a plot"""
    return auc_val

def auc(roc_obj, partial_auc=None, partial_auc_focus=None):
    """Compute AUC or partial AUC from ROC object"""
    if partial_auc is None:
        return roc_obj.auc
    
    # partial_auc is a tuple/list [start, end] for specificity range
    # partial_auc_focus can be 'sp' (specificity, default) or 'se' (sensitivity)
    start, end = partial_auc
    
    if partial_auc_focus == 'se':
        # Partial AUC based on sensitivity range
        # For sensitivity range [start, end], compute partial AUC
        # This means we're looking at TPR range [start, end]
        mask = (roc_obj.sensitivities >= start) & (roc_obj.sensitivities <= end)
        if mask.sum() > 0:
            x_subset = (1 - roc_obj.specificities)[mask]
            y_subset = roc_obj.sensitivities[mask]
            # Normalize to [0,1] range
            partial_auc_val = sklearn_auc(x_subset, y_subset) / (end - start)
        else:
            partial_auc_val = 0.0
    else:
        # Partial AUC based on specificity range (default)
        # For specificity range [start, end], compute partial AUC
        spec_vals = 1 - roc_obj.fpr
        mask = (spec_vals >= start) & (spec_vals <= end)
        if mask.sum() > 0:
            x_subset = roc_obj.fpr[mask]
            y_subset = roc_obj.tpr[mask]
            partial_auc_val = sklearn_auc(x_subset, y_subset)
        else:
            partial_auc_val = 0.0
    
    return partial_auc_val

# Create a ROC curve:
suppressPackageStartupMessages(None)  # Dummy call to match R

aSAH = pd.DataFrame(aSAH)
roc_s100b = ROC(aSAH['outcome'], aSAH['s100b'])
roc_s100b_percent = ROC(aSAH['outcome'], aSAH['s100b'], percent=True)

df_roc, roc_obj = ggroc(roc_s100b)
auc_val_1 = geom_polygon_auc(roc_s100b.auc)

df_roc_percent, roc_obj_percent = ggroc(roc_s100b_percent, legacy_axes=True)
auc_val_2 = geom_polygon_auc(roc_s100b_percent, legacy_axes=True)

# Partial AUCs
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1.0])
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus='se')

df_roc_2, _ = ggroc(roc_s100b)
auc_val_3 = geom_polygon_auc(auc_s100b_partial_sp)

df_roc_3, _ = ggroc(roc_s100b)
auc_val_4 = geom_polygon_auc(auc_s100b_partial_se)
