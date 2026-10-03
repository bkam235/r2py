# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

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
from plotnine import *

# r2py:entity:roc.s100b
def pROC_roc(response, predictor, percent=False):
    # pROC levels: [1] control, [2] case
    # aSAH$outcome levels: ["Good", "Poor"] -> Good is control, Poor is case
    # Predictor must be numeric
    predictor = np.array(predictor)
    response = np.array(response)
    
    controls = predictor[response == 'Good']
    cases = predictor[response == 'Poor']
    
    # pROC calculates ROC by iterating through thresholds
    # We combine all unique values as thresholds
    thresholds = np.unique(np.concatenate([controls, cases]))
    thresholds = np.sort(thresholds)[::-1] # Descending
    
    sensitivities = []
    specificities = []
    
    # pROC's default algorithm usually involves calculating TPR and FPR at thresholds
    # To match R exactly, we need to be careful about how it handles ties
    for t in thresholds:
        # Case: predictor >= threshold
        se = np.sum(cases >= t) / len(cases) if len(cases) > 0 else 0
        sp = np.sum(controls < t) / len(controls) if len(controls) > 0 else 0
        sensitivities.append(se)
        specificities.append(sp)
        
    # pROC ensures points (0,0) and (1,1) are present
    # Sensitivities go 0 -> 1, Specificities go 1 -> 0
    # R results for aSAH show sensitivities start at 1 and end at 0
    # This means pROC sorts them such that specificity is 0 to 1 (or vice versa)
    
    # Let's refine: pROC's roc() returns sensitivities and specificities 
    # corresponding to the thresholds.
    
    # According to the R output provided:
    # sens: [1, 0.9756, ..., 0], spec: [0, 0, 0.0694, ..., 1]
    # This means thresholds were sorted such that SE goes 1 -> 0 and SP goes 0 -> 1.
    
    # Re-calculating to match:
    all_thresholds = np.sort(np.concatenate([controls, cases]))
    # In pROC, the thresholds are typically the unique values of the predictor
    # If direction="auto", it determines whether higher or lower values are 'cases'
    # For s100b, higher values usually indicate 'Poor' (case)
    
    final_se = []
    final_sp = []
    final_thr = []
    
    # pROC calculates SE and SP for each unique threshold
    # then adds the endpoints.
    unique_thr = np.unique(predictor)
    # Sort thresholds descending to get SE 1 -> 0, SP 0 -> 1
    for t in sorted(unique_thr, reverse=True):
        se = np.mean(cases >= t)
        sp = np.mean(controls < t)
        final_se.append(se)
        final_sp.append(sp)
        final_thr.append(t)
        
    # Add endpoints to match pROC exactly
    # R output shows sens starting at 1 (sp=0) and ending at 0 (sp=1)
    # Our loop: t=max -> se=min, sp=min. t=min -> se=max, sp=max.
    # We need to reverse to get the R sequence.
    final_se = final_se[::-1]
    final_sp = final_sp[::-1]
    final_thr = final_thr[::-1]
    
    # Ensure endpoints (0,1) and (1,0)
    if final_se[0] != 1.0:
        final_se.insert(0, 1.0)
        final_sp.insert(0, 0.0)
        final_thr.insert(0, np.inf)
    if final_se[-1] != 0.0:
        final_se.append(0.0)
        final_sp.append(1.0)
        final_thr.append(-np.inf)
        
    # AUC calculation (trapezoidal)
    # auc = sum((se[i] + se[i-1])/2 * (sp[i] - sp[i-1]))
    # sp goes 0 -> 1, so sp[i] - sp[i-1] is positive
    auc_val = 0.0
    for i in range(1, len(final_se)):
        auc_val += (final_se[i] + final_se[i-1]) / 2 * (final_sp[i] - final_sp[i-1])
    
    res = {
        'sensitivities': final_se,
        'specificities': final_sp,
        'thresholds': final_thr,
        'percent': percent,
        'auc': auc_val * (10000 if percent else 1)
    }
    
    if percent:
        res['sensitivities'] = [x * 100 for x in final_se]
        res['specificities'] = [x * 100 for x in final_sp]
        
    return res

# r2py:entity:auc.s100b.partial.sp
def pROC_auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    percent = roc_obj['percent']
    # partial_auc is [high, low] e.g. [0.9, 1]
    p_high, p_low = sorted(partial_auc, reverse=True)
    
    if partial_auc_focus == "sensitivity":
        x = np.array(roc_obj['sensitivities'])
        y = np.array(roc_obj['specificities'])
    else:
        x = np.array(roc_obj['specificities'])
        y = np.array(roc_obj['sensitivities'])
        
    # pROC logic for partial AUC involves interpolation at the boundaries
    # and sum of trapezoids in between.
    
    # Filter points strictly inside
    mask = (x <= p_high) & (x >= p_low)
    x_inc = x[mask]
    y_inc = y[mask]
    
    # To match R, we need to handle the boundaries by interpolating
    # the y value at exactly x = p_high and x = p_low
    
    def get_y_at(target_x, full_x, full_y):
        if target_x in full_x:
            return full_y[np.where(full_x == target_x)[0][0]]
        # Linear interpolation
        idx = np.searchsorted(full_x, target_x)
        if idx == 0: return full_y[0]
        if idx == len(full_x): return full_y[-1]
        x0, x1 = full_x[idx-1], full_x[idx]
        y0, y1 = full_y[idx-1], full_y[idx]
        return y0 + (target_x - x0) * (y1 - y0) / (x1 - x0)

    # Ensure x is sorted for interpolation
    sort_idx = np.argsort(x)
    x_sorted, y_sorted = x[sort_idx], y[sort_idx]
    
    y_start = get_y_at(p_low, x_sorted, y_sorted)
    y_end = get_y_at(p_high, x_sorted, y_sorted)
    
    # Points for integration
    interp_x = [p_low] + x_inc[np.argsort(x_inc)].tolist() + [p_high]
    # This is a simplification; R does a more complex interpolation.
    # Let's use the trapz on a clipped and interpolated set.
    
    # Correct approach: find all x in [p_low, p_high], add boundaries
    x_pts = []
    y_pts = []
    
    # Boundary low
    x_pts.append(p_low)
    y_pts.append(get_y_at(p_low, x_sorted, y_sorted))
    
    # Middle points
    mid_mask = (x_sorted > p_low) & (x_sorted < p_high)
    x_pts.extend(x_sorted[mid_mask])
    y_pts.extend(y_sorted[mid_mask])
    
    # Boundary high
    x_pts.append(p_high)
    y_pts.append(get_y_at(p_high, x_sorted, y_sorted))
    
    p_auc = np.trapz(y_pts, x_pts)
    
    # Adjust for percent
    if percent:
        # In R, if percent=TRUE, AUC is scaled by 100*100
        # but partial AUC is usually raw area in percent units?
        # Actually, R's auc() for partial.auc just integrates the values.
        pass
        
    return p_auc

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    spec = np.array(roc_obj['specificities'])
    sens = np.array(roc_obj['sensitivities'])
    one_or_hundred = 100 if roc_obj['percent'] else 1
    
    if legacy_axes:
        x_vals = one_or_hundred - spec
    else:
        x_vals = spec
        
    df = pd.DataFrame({'x': x_vals, 'y': sens})
    p = (ggplot(df, aes(x='x', y='y')) + geom_line())
    
    if not legacy_axes:
        p = p + scale_x_reverse()
        
    return p

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(auc_val, roc_obj=None, legacy_axes=False):
    # If auc_val is a scalar and roc_obj is provided, it's like geom_polygon_auc.auc
    if roc_obj is None:
        return geom_polygon(aes(x='x', y='y'), fill="grey", alpha=0.5)

    spec = np.array(roc_obj['specificities'])
    sens = np.array(roc_obj['sensitivities'])
    one_or_hundred = 100 if roc_obj['percent'] else 1
    
    if legacy_axes:
        x_vals = one_or_hundred - spec
    else:
        x_vals = spec
    
    # The polygon covers the area under the ROC curve
    # Points: (x,y) -> (x,0) -> (min_x, 0) -> (min_x, y_at_min_x)
    if legacy_axes:
        # x is 1-spec (0 to 1). Area is from 0 to x_max.
        poly_x = np.concatenate([x_vals, [x_vals[-1]], [0], [0]])
        poly_y = np.concatenate([sens, [0], [0], [sens[0]]])
    else:
        # x is spec (1 to 0). Area is from x to 1.
        poly_x = np.concatenate([x_vals, [x_vals[-1]], [one_or_hundred], [one_or_hundred]])
        poly_y = np.concatenate([sens, [0], [0], [sens[0]]])
        
    df_poly = pd.DataFrame({'x': poly_x, 'y': poly_y})
    return geom_polygon(aes(x='x', y='y'), data=df_poly, fill="grey", alpha=0.5)

# Execution
aSAH_df = pd.DataFrame(aSAH)

# r2py:entity:roc.s100b
roc_s100b = pROC_roc(aSAH_df['outcome'], aSAH_df['s100b'])
globals()['roc.s100b'] = roc_s100b

# r2py:entity:roc.s100b.percent
roc_s100b_percent = pROC_roc(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)
globals()['roc.s100b.percent'] = roc_s100b_percent

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# r2py:entity:ggroc_1
ggroc_1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b['auc'], roc_obj=roc_s100b)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# r2py:entity:ggroc_2
ggroc_2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent['auc'], roc_obj=roc_s100b_percent, legacy_axes=True)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = pROC_auc(roc_s100b, partial_auc=[0.9, 1])
globals()['auc.s100b.partial.sp'] = auc_s100b_partial_sp

# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = pROC_auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="sensitivity")
globals()['auc.s100b.partial.se'] = auc_s100b_partial_se

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# r2py:entity:geom_polygon_auc_2
ggroc_3 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp, roc_obj=roc_s100b)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# r2py:entity:geom_polygon_auc_3
ggroc_4 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se, roc_obj=roc_s100b)