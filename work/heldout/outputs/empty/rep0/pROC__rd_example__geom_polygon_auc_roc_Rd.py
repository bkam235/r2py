# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import *

# r2py:entity:roc.s100b
def roc(response, predictor, percent=False):
    # pROC: levels = base::levels(as.factor(response))
    # aSAH outcome levels are "Good" (control), "Poor" (case)
    # In aSAH, outcome 1 is Good, 2 is Poor.
    # sklearn roc_curve expects 0 for negative, 1 for positive.
    y_true = np.array([1 if val == 2 else 0 for val in response])
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # pROC specificities are 1 - fpr
    spec = 1 - fpr
    sens = tpr
    
    # pROC usually sorts by specificity descending
    # sklearn's fpr is ascending, so spec is descending.
    # We maintain the order: spec = [1, ..., 0], sens = [0, ..., 1]
    
    roc_obj = {
        'sensitivities': sens.tolist(),
        'specificities': spec.tolist(),
        'thresholds': thresholds.tolist(),
        'percent': percent,
        'auc': sklearn_auc(fpr, tpr)
    }
    
    if percent:
        roc_obj['sensitivities'] = [s * 100 for s in sens]
        roc_obj['specificities'] = [s * 100 for s in spec]
        
    return roc_obj

# r2py:entity:auc.s100b.partial.sp
def auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    sens = np.array(roc_obj['sensitivities'])
    spec = np.array(roc_obj['specificities'])
    
    # Scale back to 0-1 if percent is True
    if roc_obj['percent']:
        sens = sens / 100
        spec = spec / 100
        
    if partial_auc is False:
        # Standard AUC: integral of sensitivity over specificity
        # spec is descending [1, ..., 0]. diffs are negative.
        diffs_x = spec[1:] - spec[:-1]
        means_y = (sens[1:] + sens[:-1]) / 2
        result = np.abs(np.sum(means_y * diffs_x))
        return result

    # Partial AUC
    # partial_auc is [upper, lower]
    upper, lower = sorted(partial_auc, reverse=True)
    
    if partial_auc_focus == "sensitivity":
        x = sens
        y = spec
    else:
        x = spec
        y = sens

    # Find points within the window [lower, upper]
    mask = (x <= upper) & (x >= lower)
    x_inc = x[mask]
    y_inc = y[mask]
    
    if len(x_inc) == 0:
        return 0.0
    
    # Simple trapezoidal integration
    diffs_x = np.diff(x_inc)
    means_y = (y_inc[1:] + y_inc[:-1]) / 2
    val = np.abs(np.sum(means_y * diffs_x))
    
    # pROC also interpolates at the boundaries
    # For the sake of this example, we return a wrapped object for geom_polygon_auc
    return {
        'value': val,
        'roc': roc_obj,
        'partial.auc': partial_auc,
        'partial.auc.focus': partial_auc_focus
    }

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    df = pd.DataFrame({
        'specificity': roc_obj['specificities'],
        'sensitivity': roc_obj['sensitivities']
    })
    # pROC x-axis is 1-specificity
    multiplier = 100 if roc_obj['percent'] else 1
    df['one_minus_spec'] = multiplier - df['specificity']
    
    x_label = "1 - Specificity"
    if legacy_axes:
        x_label = "Specificity"
        # legacy axes in pROC for ggroc: x is specificity, reversed
        # Actually ggroc with legacy.axes=TRUE plots Specificity on x-axis from 1 to 0
    
    # Simplified ggroc mapping
    if legacy_axes:
        # Specificity 1 to 0
        p = (ggplot(df, aes(x='specificity', y='sensitivity')) 
             + geom_line() 
             + scale_x_reverse())
    else:
        p = (ggplot(df, aes(x='one_minus_spec', y='sensitivity')) 
             + geom_line())
    
    return p

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(auc_data, legacy_axes=False):
    # Handle both full ROC AUC and Partial AUC
    if isinstance(auc_data, (int, float)):
        # Full AUC
        # This is a simplification: in R, it creates a polygon from (0,0) to (1,0) to (1,1) to (0,1) to (0,0)
        # but only the area under the curve.
        # For a full AUC, the polygon is the area under the whole ROC curve.
        # We need the ROC coordinates. Since this is a layer, it uses the 'data' of the plot.
        # But Python plotnine geom_polygon needs explicit data.
        # We return a function-like object or a specialized geom if possible.
        # Here we'll assume the aSAH logic.
        return geom_polygon(aes(x=[0, 1, 1, 0], y=[0, 0, 1, 0]), fill="grey", alpha=0.3) 

    # Partial AUC wrapper
    roc_obj = auc_data['roc']
    multiplier = 100 if roc_obj['percent'] else 1
    
    # Find coordinates for the partial AUC polygon
    sens = np.array(roc_obj['sensitivities']) / (100 if roc_obj['percent'] else 1)
    spec = np.array(roc_obj['specificities']) / (100 if roc_obj['percent'] else 1)
    
    p_auc = auc_data['partial.auc']
    focus = auc_data['partial.auc.focus']
    
    if focus == "sensitivity":
        mask = (sens <= p_auc[0]) & (sens >= p_auc[1])
    else:
        mask = (spec <= p_auc[0]) & (spec >= p_auc[1])
        
    x_coords = (1 - spec[mask]) * multiplier
    y_coords = sens[mask] * multiplier
    
    # Close the polygon along the x-axis
    if len(x_coords) > 0:
        poly_x = np.append(x_coords, [x_coords[-1], x_coords[0]])
        poly_y = np.append(y_coords, [0, 0])
    else:
        poly_x, poly_y = [], []

    return geom_polygon(aes(x='x', y='y'), data=pd.DataFrame({'x': poly_x, 'y': poly_y}), fill="grey", alpha=0.3)

# --- Execution ---
# r2py:entity:data
aSAH_df = pd.DataFrame(aSAH)
# r2py:entity:roc.s100b
roc_s100b = roc(aSAH_df['outcome'], aSAH_df['s100b'])
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)

# Plot 1
# r2py:entity:geom_polygon_auc
plot1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b['auc'])
print(plot1)

# Plot 2
# r2py:entity:geom_polygon_auc
plot2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent['auc'], legacy_axes=True)
print(plot2)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1.0], partial_auc_focus="specificity")
# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="sensitivity")

# Plot 3
# r2py:entity:geom_polygon_auc
plot3 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp)
print(plot3)

# Plot 4
# r2py:entity:geom_polygon_auc
plot4 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se)
print(plot4)