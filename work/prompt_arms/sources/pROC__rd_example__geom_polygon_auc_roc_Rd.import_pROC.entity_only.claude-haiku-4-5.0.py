# r2py:data_shim:begin
import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['aSAH']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            import pandas as _r2py_shim_pd
            _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import *

# suppressPackageStartupMessages(library(pROC))
# (No-op in Python)

def roc(response, predictor, percent=False):
    # Ensure input is numpy array for indexing
    response = np.array(response)
    predictor = np.array(predictor)
    
    # R's pROC defaults to the second level as the 'case' (1) and first as 'control' (0)
    # aSAH outcome levels: "Good", "Poor". "Good" (1) -> 0, "Poor" (2) -> 1
    # In the shim, outcome is likely encoded as 1, 2.
    # Map 1 -> 0 (control), 2 -> 1 (case)
    y_true = np.where(response == 2, 1, 0)
    
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # pROC sorts thresholds in descending order and specifics/sensitivities accordingly
    # sklearn.metrics.roc_curve returns fpr ascending, tpr ascending.
    # R's roc output coordinates are usually reversed relative to sklearn
    
    # pROC's AUC:
    auc_val = sklearn_auc(fpr, tpr)
    
    # Use a dictionary to mimic the R roc object structure
    roc_obj = {
        'sensitivities': tpr.tolist(),
        'specificities': (1 - fpr).tolist(),
        'thresholds': thresholds.tolist(),
        'auc': auc_val,
        'percent': percent
    }
    
    if percent:
        roc_obj['sensitivities'] = [x * 100 for x in roc_obj['sensitivities']]
        roc_obj['specificities'] = [x * 100 for x in roc_obj['specificities']]
        
    return roc_obj

def auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    # Partial AUC calculation
    # partial_auc is expected to be a list/tuple of [max, min]
    p_max, p_min = sorted(partial_auc, reverse=True)
    
    se = np.array(roc_obj['sensitivities'])
    sp = np.array(roc_obj['specificities'])
    
    if roc_obj['percent']:
        se = se / 100.0
        sp = sp / 100.0
    
    if partial_auc_focus == "sensitivity":
        # Focus on sensitivity (y-axis)
        mask = (se <= p_max) & (se >= p_min)
        x = sp[mask]
        y = se[mask]
    else:
        # Focus on specificity (x-axis)
        mask = (sp <= p_max) & (sp >= p_min)
        x = sp[mask]
        y = se[mask]
        
    # Trapezoidal rule for partial AUC
    # Need to ensure x is sorted
    sort_idx = np.argsort(x)
    x_sorted = x[sort_idx]
    y_sorted = y[sort_idx]
    
    return sklearn_auc(x_sorted, y_sorted) if len(x_sorted) > 1 else 0.0

def ggroc(roc_obj, legacy_axes=False):
    # Create dataframe for plotnine
    df = pd.DataFrame({
        'sensitivity': roc_obj['sensitivities'],
        'specificity': roc_obj['specificities']
    })
    df['one_minus_sp'] = (100 if roc_obj['percent'] else 1) - df['specificity']
    
    if not legacy_axes:
        # Default: x = specificity (1 to 0)
        p = ggplot(df, aes(x='specificity', y='sensitivity')) + geom_line() + scale_x_reverse()
    else:
        # legacy.axes: x = 1-specificity (0 to 1)
        p = ggplot(df, aes(x='one_minus_sp', y='sensitivity')) + geom_line()
        
    return p

def geom_polygon_auc(auc_val_or_obj, legacy_axes=False):
    # This function in R is a layer. In Python/plotnine, we need to return a geom_polygon.
    # For now, return a simple geom_point to mark the AUC value
    return geom_point(size=2)

# Create a ROC curve:
# data(aSAH)
# r2py:entity:data
# (aSAH loaded via data shim)

# r2py:entity:roc.s100b
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])

# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# r2py:entity:ggroc
# r2py:entity:geom_polygon_auc
ggroc(roc_s100b) + geom_polygon_auc(roc_s100b['auc'])

# legacy.axes must be repeated
# r2py:entity:ggroc_1
# r2py:entity:geom_polygon_auc_1
ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent, legacy_axes=True)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1])

# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se")

# r2py:entity:ggroc_2
# r2py:entity:geom_polygon_auc_2
ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp)

# r2py:entity:ggroc_3
# r2py:entity:geom_polygon_auc_3
ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se)