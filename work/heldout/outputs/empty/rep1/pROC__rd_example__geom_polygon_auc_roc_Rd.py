# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

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
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import *

def set_r_var(name, value):
    globals()[name] = value

# r2py:entity:roc.s100b
def roc(response, predictor, percent=False):
    # aSAH outcome: "Good" (control), "Poor" (case)
    y_true = np.where(response == "Poor", 1, 0)
    
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # pROC sorts specificities descending (1 -> 0)
    sp = 1 - fpr
    se = tpr
    
    auc_val = sklearn_auc(fpr, tpr)
    
    # Map to R's pROC structure more closely
    roc_obj = {
        'sensitivities': se.tolist(),
        'specificities': sp.tolist(),
        'thresholds': thresholds.tolist(),
        'percent': percent,
        'auc': auc_val,
        'levels': ["Good", "Poor"],
        'response': response,
        'predictor': predictor,
        'direction': '<',
        'cases': np.sum(y_true == 1),
        'controls': np.sum(y_true == 0),
        'call': 'roc(aSAH$outcome, aSAH$s100b)'
    }
    
    if percent:
        roc_obj['sensitivities'] = (se * 100).tolist()
        roc_obj['specificities'] = (sp * 100).tolist()
        
    return roc_obj

# r2py:entity:auc.s100b.partial.sp
def auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    percent = roc_obj['percent']
    se = np.array(roc_obj['sensitivities'])
    sp = np.array(roc_obj['specificities'])
    
    # If percent is True, coordinates are 0-100. R's auc.roc handles this.
    # But partial_auc limits are usually 0-1 unless specified otherwise.
    # In the example: auc(roc.s100b, partial.auc = c(0.9, 1))
    
    if partial_auc is False:
        # Simple trapezoidal rule: sum((y_i + y_{i-1})/2 * (x_i - x_{i-1}))
        # pROC: sum(means.vert * diffs.x)
        diffs_x = sp[1:] - sp[:-1]
        means_vert = (se[1:] + se[:-1]) / 2
        return np.sum(means_vert * diffs_x)
    
    # partial_auc = [upper, lower] sorted descending
    p_auc = sorted(partial_auc, reverse=True)
    
    if partial_auc_focus == "sensitivity":
        x, y = se[::-1], sp[::-1] # R: rev(se), rev(sp)
    else:
        x, y = sp, se
    
    # R logic: x.inc <- x[x <= partial.auc[1] & x >= partial.auc[2]]
    mask = (x <= p_auc[0]) & (x >= p_auc[1])
    x_inc = x[mask]
    y_inc = y[mask]
    
    if len(x_inc) == 0:
        # Linear interpolation between surrounding points
        idx_hi = np.searchsorted(x, p_auc[0], side='left')
        idx_lo = idx_hi - 1
        # Avoid index out of bounds
        idx_hi = min(max(idx_hi, 1), len(x)-1)
        idx_lo = min(max(idx_lo, 0), len(x)-2)
        
        diff_horiz = p_auc[0] - p_auc[1]
        prop_hi = (x[idx_hi] - p_auc[0]) / (x[idx_hi] - x[idx_lo]) if x[idx_hi] != x[idx_lo] else 0
        prop_lo = (p_auc[1] - x[idx_lo]) / (x[idx_hi] - x[idx_lo]) if x[idx_hi] != x[idx_lo] else 0
        
        y_hi = y[idx_hi] + prop_hi * (y[idx_lo] - y[idx_hi])
        y_lo = y[idx_lo] - prop_lo * (y[idx_lo] - y[idx_hi])
        return ((y_hi + y_lo) / 2) * diff_horiz

    # Trapezoidal sum for the inner points
    diffs_x = x_inc[1:] - x_inc[:-1]
    means_vert = (y_inc[1:] + y_inc[:-1]) / 2
    res_auc = np.sum(means_vert * diffs_x)
    
    # Boundary interpolation
    if not any(x_inc == p_auc[0]):
        idx_out = np.searchsorted(x, p_auc[0], side='left')
        idx_in = idx_out - 1
        if 0 <= idx_in < len(x) and 0 <= idx_out < len(x):
            prop = (p_auc[0] - x[idx_out]) / (x[idx_in] - x[idx_out]) if x[idx_in] != x[idx_out] else 0
            y_interp = y[idx_out] + prop * (y[idx_in] - y[idx_out])
            res_auc += (p_auc[0] - x[idx_in]) * (y[idx_in] + y_interp) / 2
            
    if not any(x_inc == p_auc[1]):
        idx_out = np.searchsorted(x, p_auc[1], side='right') - 1
        idx_in = idx_out + 1
        if 0 <= idx_in < len(x) and 0 <= idx_out < len(x):
            prop = (x[idx_in] - p_auc[1]) / (x[idx_in] - x[idx_out]) if x[idx_in] != x[idx_out] else 0
            y_interp = y[idx_in] + prop * (y[idx_out] - y[idx_in])
            res_auc += (x[idx_in] - p_auc[1]) * (y[idx_in] + y_interp) / 2
            
    return res_auc

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    percent = roc_obj['percent']
    sp = np.array(roc_obj['specificities'])
    se = np.array(roc_obj['sensitivities'])
    
    if legacy_axes:
        x_vals = (100 if percent else 1) - sp
    else:
        x_vals = sp
        
    df = pd.DataFrame({'x': x_vals, 'y': se})
    p = (ggplot(df, aes(x='x', y='y')) + geom_line())
    
    if not legacy_axes:
        p = p + scale_x_reverse()
        
    return p

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(auc_input, roc_obj=None, legacy_axes=False):
    if roc_obj is None:
        return geom_polygon()
        
    percent = roc_obj['percent']
    one_or_hundred = 100 if percent else 1
    sp = np.array(roc_obj['specificities'])
    se = np.array(roc_obj['sensitivities'])
    
    if legacy_axes:
        x_vals = one_or_hundred - sp
    else:
        x_vals = sp
    
    poly_x = np.append(x_vals, [x_vals[-1], x_vals[0]])
    poly_y = np.append(se, [0, 0])
    
    poly_df = pd.DataFrame({'x': poly_x, 'y': poly_y})
    return geom_polygon(aes(x='x', y='y'), data=poly_df, fill="grey", alpha=0.5)

# --- Execution ---
suppressPackageStartupMessages = lambda x: None

# r2py:entity:data
aSAH_df = pd.DataFrame(aSAH)

# r2py:entity:roc.s100b
roc_s100b = roc(aSAH_df['outcome'], aSAH_df['s100b'])
set_r_var('roc.s100b', roc_s100b)

# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)
set_r_var('roc.s100b.percent', roc_s100b_percent)

# r2py:entity:geom_polygon_auc
plot1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b['auc'], roc_obj=roc_s100b)

# r2py:entity:geom_polygon_auc_1
plot2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent['auc'], roc_obj=roc_s100b_percent, legacy_axes=True)

# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1], partial_auc_focus="specificity")
set_r_var('auc.s100b.partial.sp', auc_s100b_partial_sp)

# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="sensitivity")
set_r_var('auc.s100b.partial.se', auc_s100b_partial_se)

# r2py:entity:geom_polygon_auc_2
plot3 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp, roc_obj=roc_s100b)
# r2py:entity:geom_polygon_auc_3
plot4 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se, roc_obj=roc_s100b)