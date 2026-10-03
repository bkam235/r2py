# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260929_162051/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import ggplot, aes, geom_line, geom_polygon, scale_x_continuous

# --- Data Setup ---
# Manual translation of aSAH data structure provided in source
# r2py:entity:data
aSAH_data = {
    'outcome': [1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1],
    's100b': [0.13, 0.14, 0.1, 0.04, 0.13, 0.1, 0.47, 0.16, 0.18, 0.1, 0.12, 0.1, 0.44, 0.71, 0.04, 0.08, 0.49, 0.04, 0.07, 0.33, 0.09, 0.09, 0.07, 0.11, 0.07, 0.17, 0.07, 0.11, 0.13, 0.19, 0.05, 0.16, 0.41, 0.14, 0.34, 0.35, 0.48, 0.09, 0.96, 0.25, 0.5, 0.46, 0.16, 0.07, 0.43, 0.45, 0.11, 0.08, 0.09, 0.86, 0.52, 0.08, 0.06, 0.13, 2.07, 0.1, 0.14, 0.15, 0.07, 0.06, 0.77, 0.05, 0.09, 0.3, 0.03, 0.09, 0.04, 0.23, 0.7, 0.09, 0.27, 0.71, 0.08, 0.26, 0.08, 0.16, 0.09, 0.13, 0.1, 0.08, 0.11, 0.33, 0.11, 0.28, 0.07, 0.1, 0.32, 0.22, 0.07, 0.05, 0.24, 0.38, 0.1, 0.15, 0.08, 0.14, 0.1, 0.07, 0.04, 0.19, 0.56, 0.14, 0.58, 0.32, 0.82, 0.74, 0.15, 0.47, 0.17, 0.44, 0.15, 0.5, 0.48]
}

# --- Implement pROC-like functionality ---

# r2py:entity:roc.s100b
def roc(response, predictor, percent=False):
    # Map outcomes: Good(1) -> 0, Poor(2) -> 1
    y_true = np.where(np.array(response) == 2, 1, 0)
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    multiplier = 100 if percent else 1
    return {
        'sensitivities': tpr * multiplier,
        'specificities': (1 - fpr) * multiplier,
        'thresholds': thresholds,
        'auc': sklearn_auc(fpr, tpr),
        'percent': percent
    }

# r2py:entity:auc.s100b.partial.sp
def auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    # Logic for partial AUC calculation based on provided R helper
    se = roc_obj['sensitivities'] / (100 if roc_obj['percent'] else 1)
    sp = roc_obj['specificities'] / (100 if roc_obj['percent'] else 1)
    
    # sort for trapezoidal integration
    idx = np.argsort(sp)
    sp, se = sp[idx], se[idx]
    
    if partial_auc_focus == "sensitivity":
        # x = sensitivity, y = specificity
        x, y = se, sp
    else:
        # x = specificity, y = sensitivity
        x, y = sp, se
    
    # In pROC, partial.auc is usually [upper, lower]
    upper, lower = sorted(partial_auc, reverse=True)
    
    mask = (x <= upper) & (x >= lower)
    x_inc, y_inc = x[mask], y[mask]
    
    # Basic trapezoidal rule for the segment
    if len(x_inc) < 2:
        return 0.0 # Simplified for this context
    
    return np.trapz(y_inc, x_inc)

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    multiplier = 100 if roc_obj['percent'] else 1
    df = pd.DataFrame({
        'specificity': roc_obj['specificities'],
        'sensitivity': roc_obj['sensitivities'],
        '1-specificity': multiplier - roc_obj['specificities']
    })
    
    x_col = 'specificity' if legacy_axes else '1-specificity'
    # R's ggroc uses a specific axis direction
    return ggplot(df, aes(x=x_col, y='sensitivity')) + geom_line()

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(auc_val, roc_obj=None, legacy_axes=False):
    # In R, this is a ggplot layer. In Python, we generate a polygon dataframe.
    multiplier = 100 if (roc_obj and roc_obj['percent']) else 1
    
    # Simplified polygon creation for AUC visualization
    # Typical AUC polygon: (0,0), (0,1), (1,1), (0,0) for full AUC
    # For partial AUC, the bounds change.
    if not roc_obj:
        # Assume full AUC if no roc_obj provided
        poly_df = pd.DataFrame({
            'x': [0, 0, multiplier, 0],
            'y': [0, multiplier, multiplier, 0]
        })
    else:
        # Use the coords from the roc object to build a polygon
        poly_df = pd.DataFrame({
            'x': list(multiplier - roc_obj['specificities']) + [0],
            'y': list(roc_obj['sensitivities']) + [0]
        })
    
    x_col = 'specificity' if legacy_axes else 'x'
    return geom_polygon(aes(x=x_col, y='y'), data=poly_df)

# --- Main Script Translation ---

# Create a ROC curve
# r2py:entity:roc.s100b
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Plot 1
# r2py:entity:geom_polygon_auc
p1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b['auc'], roc_obj=roc_s100b)

# Plot 2 (legacy axes)
# r2py:entity:geom_polygon_auc
p2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent['auc'], roc_obj=roc_s100b_percent, legacy_axes=True)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1])
# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se")

# Plot 3 & 4
# r2py:entity:geom_polygon_auc
p3 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp, roc_obj=roc_s100b)
# r2py:entity:geom_polygon_auc
p4 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se, roc_obj=roc_s100b)