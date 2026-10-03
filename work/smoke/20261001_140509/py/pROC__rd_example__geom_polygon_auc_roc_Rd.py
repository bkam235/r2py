# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_140509/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import ggplot, aes, geom_line, geom_polygon, scale_x_continuous

# Recreate aSAH dataset

# r2py:entity:roc.s100b
def roc(response, predictor, percent=False):
    # Convert response to binary (1=Control, 2=Case as per R factor levels "Good", "Poor")
    y_true = (response == 2).astype(int)
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # pROC's roc object stores specificities and sensitivities
    # specificities = 1 - fpr
    res = {
        'sensitivities': tpr,
        'specificities': 1 - fpr,
        'thresholds': thresholds,
        'percent': percent,
        'auc': sklearn_auc(fpr, tpr) * (10000 if percent else 1)
    }
    if percent:
        res['auc'] = sklearn_auc(fpr, tpr) * 100
    else:
        res['auc'] = sklearn_auc(fpr, tpr)
    return res

# r2py:entity:auc.s100b.partial.sp
def auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    # partial_auc is a list/tuple [high, low]
    high, low = sorted(partial_auc, reverse=True)
    
    if partial_auc_focus == "sensitivity":
        # integrate over sensitivity
        x = roc_obj['sensitivities']
        y = roc_obj['specificities']
    else:
        # integrate over specificity
        x = roc_obj['specificities']
        y = roc_obj['sensitivities']
        
    mask = (x <= high) & (x >= low)
    x_inc = x[mask]
    y_inc = y[mask]
    
    # Simple trapezoidal integration for the partial area
    # Note: pROC does linear interpolation for partial AUC edges. 
    # This is a simplified approximation.
    if len(x_inc) < 2:
        return 0.0
    
    return np.trapz(y_inc, x_inc)

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    percent_val = 100 if roc_obj['percent'] else 1
    df = pd.DataFrame({
        'specificity': roc_obj['specificities'],
        'sensitivity': roc_obj['sensitivities']
    })
    df['1-specificity'] = percent_val - df['specificity']
    
    # R's ggroc plots sensitivity vs 1-specificity (or specificity)
    # Legacy axes often flip the x-axis or scale it
    p = ggplot(df, aes(x='1-specificity', y='sensitivity')) + geom_line()
    if legacy_axes:
        p = p + scale_x_continuous(limits=(0, percent_val))
    return p

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(auc_val, roc_obj=None, legacy_axes=False):
    # This function in R adds a polygon layer. 
    # Since we can't return a 'layer' object easily like ggplot2, 
    # we will integrate this logic into the plot call in the main script.
    # For the translation, we'll return the data needed for the polygon.
    percent_val = 100 if (roc_obj['percent'] if roc_obj else False) else 1
    
    # Create polygon coordinates
    # Based on the R source, it adds points to close the shape from the ROC curve to the axes
    df = pd.DataFrame({
        '1-specificity': (percent_val - roc_obj['specificities']),
        'sensitivity': roc_obj['sensitivities']
    })
    
    # Add points to close the polygon to the origin (0,0)
    # Simplified version of geom_polygon_auc logic
    poly_df = pd.concat([df, pd.DataFrame({'1-specificity': [0], 'sensitivity': [0]})], ignore_index=True)
    return geom_polygon(aes(x='1-specificity', y='sensitivity'), data=poly_df)

# Execution
# r2py:entity:roc.s100b
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Plot 1
# r2py:entity:geom_polygon_auc
p1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b['auc'], roc_obj=roc_s100b)

# Plot 2
# r2py:entity:geom_polygon_auc_1
p2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent['auc'], roc_obj=roc_s100b_percent, legacy_axes=True)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1])
# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se")

# The R script uses auc_val as the first arg to geom_polygon_auc, 
# but needs the roc_obj to determine coordinates.
# r2py:entity:geom_polygon_auc_2
p3 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp, roc_obj=roc_s100b)
# r2py:entity:geom_polygon_auc_3
p4 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se, roc_obj=roc_s100b)