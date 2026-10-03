# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import ggplot, aes, geom_line, geom_polygon, scale_x_continuous

# Create the aSAH dataset based on the provided R structure

# r2py:entity:roc.s100b
def roc(response, predictor, percent=False):
    # pROC's roc usually considers the second level as the case. 
    # In aSAH, outcome 1 is 'Good', 2 is 'Poor'. 
    # We map Poor(2) to 1 and Good(1) to 0 for sklearn
    y_true = (response == 2).astype(int)
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # R pROC specificity is 1 - fpr
    specificity = 1 - fpr
    
    multiplier = 100 if percent else 1
    return {
        'sensitivities': tpr * multiplier,
        'specificities': specificity * multiplier,
        'thresholds': thresholds,
        'auc': sklearn_auc(fpr, tpr),
        'percent': percent
    }

# r2py:entity:auc.s100b.partial.sp
def auc_partial(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    # partial_auc is expected as [upper, lower] (sorted decreasingly in R)
    upper, lower = sorted(partial_auc, reverse=True)
    
    if partial_auc_focus == "sensitivity":
        x = roc_obj['sensitivities']
        y = roc_obj['specificities']
    else:
        x = roc_obj['specificities']
        y = roc_obj['sensitivities']
        
    mask = (x <= upper) & (x >= lower)
    x_part = x[mask]
    y_part = y[mask]
    
    # Trapezoidal rule for partial AUC
    if len(x_part) < 2:
        return 0.0
    
    return np.trapz(y_part, x_part)

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    multiplier = 100 if roc_obj['percent'] else 1
    df = pd.DataFrame({
        'specificity': roc_obj['specificities'],
        'sensitivity': roc_obj['sensitivities'],
        '1-specificity': multiplier - roc_obj['specificities']
    })
    
    x_col = '1-specificity' if not legacy_axes else '1-specificity'
    # Note: legacy.axes=TRUE in R pROC reverses the x-axis to show Specificity from 1 to 0
    # But here we follow the logic of producing a plot.
    
    plot = ggplot(df, aes(x=x_col, y='sensitivity')) + geom_line()
    if legacy_axes:
        plot = plot + scale_x_continuous(limits=(0, 100 if roc_obj['percent'] else 1))
    return plot

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(roc_or_auc, legacy_axes=False):
    # Since Python plotnine doesn't have the exact geom_polygon_auc, 
    # we create a dataframe that closes the polygon.
    if isinstance(roc_or_auc, dict):
        roc_obj = roc_or_auc
        auc_val = roc_obj['auc']
    else:
        # This handles the case where a partial AUC value is passed
        # In R, geom_polygon_auc.auc looks for the 'roc' attribute.
        # We'll simulate this by expecting a dict with 'roc' and 'value'.
        roc_obj = roc_or_auc['roc']
        auc_val = roc_or_auc['value']

    multiplier = 100 if roc_obj['percent'] else 1
    
    # Create polygon coords
    x = roc_obj['specificities'] # This is actually handled as 1-sp in plot
    y = roc_obj['sensitivities']
    
    # Simplified polygon: Area under the curve down to x-axis
    poly_df = pd.DataFrame({
        '1-specificity': np.concatenate([roc_obj['specificities'], [0], [0]]),
        'sensitivity': np.concatenate([roc_obj['sensitivities'], [0], [0]])
    })
    
    return geom_polygon(aes(x='1-specificity', y='sensitivity'), data=poly_df)

# Execute the script logic
# r2py:entity:roc.s100b
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Plot 1
# r2py:entity:geom_polygon_auc
p1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b)

# Plot 2 (legacy axes)
# r2py:entity:geom_polygon_auc
p2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent, legacy_axes=True)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc_partial(roc_s100b, partial_auc=[0.9, 1])
# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc_partial(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="sensitivity")

# Plot 3 & 4 (Partial AUC polygons)
# In R, the a.u.c. object is passed to geom_polygon_auc. 
# We wrap them to keep the ROC context.
# r2py:entity:geom_polygon_auc
p3 = ggroc(roc_s100b) + geom_polygon_auc({'roc': roc_s100b, 'value': auc_s100b_partial_sp})
# r2py:entity:geom_polygon_auc
p4 = ggroc(roc_s100b) + geom_polygon_auc({'roc': roc_s100b, 'value': auc_s100b_partial_se})