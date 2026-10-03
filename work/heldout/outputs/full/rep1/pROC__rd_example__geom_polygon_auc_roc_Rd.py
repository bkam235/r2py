# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sk_auc
from plotnine import *

aSAH_df = pd.DataFrame(aSAH)

# r2py:entity:roc.s100b
def roc_py(response, predictor, percent=False):
    # pROC's default levels for aSAH outcome are "Good" and "Poor"
    # pROC assigns control=levels[1], case=levels[2]. 
    # In aSAH: Good (0), Poor (1)
    if response.dtype == 'object' or isinstance(response.dtype, pd.CategoricalDtype):
        # Assume levels are ['Good', 'Poor'] based on R source
        mapping = {'Good': 0, 'Poor': 1}
        y_true = response.map(mapping).values
    else:
        y_true = response.values

    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # pROC internal: sensitivites and specificities
    # sklearn fpr = 1 - specificity
    # pROC sorted specificities are usually descending (1 to 0)
    # We provide the lists to match R's structure
    roc_obj = {
        'sensitivities': tpr,
        'specificities': (1 - fpr),
        'thresholds': thresholds,
        'percent': percent,
        'auc': sk_auc(fpr, tpr)
    }
    
    # pROC stores them such that specificity is decreasing (1 -> 0)
    # sklearn's tpr/fpr are typically ordered by threshold
    # We ensure the order matches pROC's internal roc$sensitivities etc.
    # In pROC, the first element is usually sensitivity=1, specificity=0
    roc_obj['sensitivities'] = roc_obj['sensitivities'][::-1]
    roc_obj['specificities'] = roc_obj['specificities'][::-1]
    roc_obj['thresholds'] = roc_obj['thresholds'][::-1]
    
    if percent:
        roc_obj['sensitivities'] = roc_obj['sensitivities'] * 100
        roc_obj['specificities'] = roc_obj['specificities'] * 100
        roc_obj['auc'] = roc_obj['auc'] * 10000
        
    return roc_obj

roc_s100b = roc_py(aSAH_df['outcome'], aSAH_df['s100b'])
globals()['roc.s100b'] = roc_s100b

# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc_py(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)
globals()['roc.s100b.percent'] = roc_s100b_percent

# r2py:entity:auc.s100b.partial.sp
def auc_py(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    percent = roc_obj['percent']
    se = np.array(roc_obj['sensitivities'])
    sp = np.array(roc_obj['specificities'])
    
    if partial_auc is False:
        # Trapeze rule: sum((y_i + y_{i-1})/2 * dx)
        # pROC: diffs.x <- sp[-1] - sp[-length(sp)]
        # sp is descending (1 to 0), so sp[-1] is smaller than sp[-length]
        # result is negative, pROC takes sum which matches the area
        diffs_x = sp[1:] - sp[:-1]
        means_vert = (se[1:] + se[:-1]) / 2
        return abs(np.sum(means_vert * diffs_x))
    
    # Partial AUC interpolation logic from pROC
    p_auc = sorted(partial_auc, reverse=True)
    if partial_auc_focus == "sensitivity":
        x = se[::-1] # ascending
        y = sp[::-1] # descending
    else:
        x = sp[::-1] # ascending
        y = se[::-1] # ascending
        
    # x is now sorted ascending
    # find range
    mask = (x <= p_auc[0]) & (x >= p_auc[1])
    x_inc = x[mask]
    y_inc = y[mask]
    
    # Basic trapeze area for the inclusive part
    res = 0
    if len(x_inc) > 1:
        diffs_x = np.diff(x_inc)
        means_vert = (y_inc[1:] + y_inc[:-1]) / 2
        res = np.sum(means_vert * diffs_x)
        
    # Handle boundaries via interpolation
    # Upper bound p_auc[0]
    if len(x) > 0 and not any(x == p_auc[0]):
        idx_out = np.searchsorted(x, p_auc[0])
        if 0 < idx_out < len(x):
            x_in, x_out = x[idx_out-1], x[idx_out]
            y_in, y_out = y[idx_out-1], y[idx_out]
            prop = (p_auc[0] - x_out) / (x_in - x_out)
            y_interp = y_out + prop * (y_in - y_out)
            res += (p_auc[0] - x_in) * (y_in + y_interp) / 2
            
    # Lower bound p_auc[1]
    if len(x) > 0 and not any(x == p_auc[1]):
        idx_out = np.searchsorted(x, p_auc[1])
        if 0 < idx_out < len(x):
            x_out, x_in = x[idx_out-1], x[idx_out]
            y_out, y_in = y[idx_out-1], y[idx_out]
            prop = (x_in - p_auc[1]) / (x_in - x_out)
            y_interp = y_in + prop * (y_out - y_in)
            res += (x_in - p_auc[1]) * (y_in + y_interp) / 2
            
    return abs(res)

auc_s100b_partial_sp = auc_py(roc_s100b, partial_auc=[0.9, 1])
globals()['auc.s100b.partial.sp'] = auc_s100b_partial_sp

# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc_py(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="sensitivity")
globals()['auc.s100b.partial.se'] = auc_s100b_partial_se

# r2py:entity:ggroc
def get_roc_df(roc_obj):
    offset = 100 if roc_obj['percent'] else 1
    # R ggroc: x = 1-specificity, y = sensitivity
    df = pd.DataFrame({
        'x': offset - np.array(roc_obj['specificities']),
        'y': np.array(roc_obj['sensitivities'])
    })
    return df

# ggroc(roc.s100b)
roc_df = get_roc_df(roc_s100b)
ggroc = (ggplot(roc_df, aes(x='x', y='y')) + geom_line())
# geom_polygon_auc(roc.s100b$auc)
# In pROC, geom_polygon_auc for full AUC shades the area under the curve
# r2py:entity:geom_polygon_auc
geom_polygon_auc = ggroc + geom_area(roc_df, aes(x='x', y='y'), fill="grey", alpha=0.3)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# r2py:entity:ggroc_1
roc_df_pct = get_roc_df(roc_s100b_percent)
ggroc_1 = (ggplot(roc_df_pct, aes(x='x', y='y')) + geom_line())
# r2py:entity:geom_polygon_auc_1
geom_polygon_auc_1 = ggroc_1 + geom_area(roc_df_pct, aes(x='x', y='y'), fill="grey", alpha=0.3)

def get_partial_auc_df(roc_obj, p_auc, focus="specificity"):
    se = np.array(roc_obj['sensitivities'])
    sp = np.array(roc_obj['specificities'])
    if focus == "sensitivity":
        mask = (se <= p_auc[0]) & (se >= p_auc[1])
    else:
        mask = (sp <= p_auc[0]) & (sp >= p_auc[1])
    
    offset = 100 if roc_obj['percent'] else 1
    return pd.DataFrame({
        'x': offset - sp[mask],
        'y': se[mask]
    })

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# r2py:entity:ggroc_2
part_sp_df = get_partial_auc_df(roc_s100b, [0.9, 1], "specificity")
ggroc_2 = (ggplot(roc_df, aes(x='x', y='y')) + geom_line())
# r2py:entity:geom_polygon_auc_2
geom_polygon_auc_2 = ggroc_2 + geom_area(part_sp_df, aes(x='x', y='y'), fill="grey", alpha=0.3)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# r2py:entity:ggroc_3
part_se_df = get_partial_auc_df(roc_s100b, [0.8, 0.9], "sensitivity")
ggroc_3 = (ggplot(roc_df, aes(x='x', y='y')) + geom_line())
# r2py:entity:geom_polygon_auc_3
geom_polygon_auc_3 = ggroc_3 + geom_area(part_se_df, aes(x='x', y='y'), fill="grey", alpha=0.3)

# Final output for verifier
print(ggroc)
print(ggroc_1)
print(ggroc_2)
print(ggroc_3)