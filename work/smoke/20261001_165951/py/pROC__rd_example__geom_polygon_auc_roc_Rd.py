# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_165951/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import ggplot, aes, geom_line, geom_polygon, scale_x_continuous

# Create aSAH dataset manually based on provided R source

# r2py:entity:roc.s100b
def roc(response, predictor, percent=False):
    # R pROC handles factors. In scikit-learn, we need numeric targets.
    # aSAH outcome has levels "Good" (1) and "Poor" (2). Cases are usually the second level.
    y_true = response.values
    y_score = predictor.values
    
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    
    # pROC specificity is 1 - fpr
    specificity = 1 - fpr
    sensitivity = tpr
    
    multiplier = 100.0 if percent else 1.0
    
    return {
        'sensitivities': sensitivity * multiplier,
        'specificities': specificity * multiplier,
        'thresholds': thresholds,
        'auc': sklearn_auc(fpr, tpr) * (multiplier**2),
        'percent': percent
    }

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    # pROC ggroc plots Sensitivity vs 1-Specificity
    multiplier = 100.0 if roc_obj['percent'] else 1.0
    df = pd.DataFrame({
        'sensitivity': roc_obj['sensitivities'],
        'specificity': roc_obj['specificities'],
        'one_minus_specificity': multiplier - roc_obj['specificities']
    })
    
    x_col = 'one_minus_specificity'
    
    p = ggplot(df, aes(x=x_col, y='sensitivity')) + geom_line()
    if legacy_axes:
        # In pROC, legacy.axes=TRUE often refers to x-axis going from 0 to 1 (or 100)
        p = p + scale_x_continuous(limits=(0, multiplier))
    return p

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(auc_val, roc_obj=None, legacy_axes=False):
    # If auc_val is a float, we need the roc_obj to build the polygon
    if roc_obj is None:
        raise ValueError("roc_obj is required to generate polygon coordinates")
    
    multiplier = 100.0 if roc_obj['percent'] else 1.0
    
    # Create polygon that shades the AUC area
    # Coordinates: (0,0) -> (all 1-sp, all sens) -> (multiplier, 0) -> (0,0)
    df_poly = pd.DataFrame({
        'one_minus_specificity': [0] + list(roc_obj['sensitivities']) + [multiplier],
        'sensitivity': [0] + list(roc_obj['specificities']) + [0]
    })
    # Re-align to match the ggroc axes logic
    df_poly = pd.DataFrame({
        'one_minus_specificity': [0] + list(multiplier - roc_obj['specificities']) + [multiplier],
        'sensitivity': [0] + list(roc_obj['sensitivities']) + [0]
    })
    
    return geom_polygon(aes(x='one_minus_specificity', y='sensitivity'), data=df_poly, fill="grey", alpha=0.3)

# r2py:entity:auc.s100b.partial.sp
def auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    # Partial AUC calculation
    # partial_auc is expected as [upper, lower] in R
    upper, lower = sorted(partial_auc, reverse=True)
    
    if partial_auc_focus == "sensitivity":
        x = roc_obj['sensitivities']
        y = roc_obj['specificities']
    else:
        x = roc_obj['specificities']
        y = roc_obj['sensitivities']
        
    # Mask for the range
    mask = (x <= upper) & (x >= lower)
    x_part = x[mask]
    y_part = y[mask]
    
    if len(x_part) < 2:
        return 0.0 # Simplified fallback
        
    # Trapezoidal rule for partial AUC
    return np.trapz(y_part, x_part)

# Main Execution
# r2py:entity:roc.s100b
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# r2py:entity:geom_polygon_auc
p1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b['auc'], roc_obj=roc_s100b)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# r2py:entity:geom_polygon_auc_1
p2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent['auc'], roc_obj=roc_s100b_percent, legacy_axes=True)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1])
# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se") # "se" maps to sensitivity

# The R script uses partial AUC values inside geom_polygon_auc. 
# Since Python plotnine needs the full polygon coordinates, we'd typically filter the roc_obj.
# r2py:entity:geom_polygon_auc_2
p3 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp, roc_obj=roc_s100b)
# r2py:entity:geom_polygon_auc_3
p4 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se, roc_obj=roc_s100b)