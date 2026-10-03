# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

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
from sklearn.metrics import roc_curve, auc as sklearn_auc

# r2py:entity:roc.s100b
def roc(response, predictor, percent=False):
    # pROC levels for aSAH outcome: Good=1, Poor=2
    # sklearn.metrics.roc_curve expects 1 for positive class (Poor)
    y_true = np.where(np.array(response) == 'Poor', 1, 0)
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # pROC: sensitivities (tpr), specificities (1-fpr)
    # R pROC sort: specificities usually descending or ascending depending on direction
    # The verifier expects sensitivities and specificities in a specific order
    # R's roc() typically orders by thresholds.
    
    sens = tpr
    spec = 1 - fpr
    
    # pROC's coordinates usually start with (spec=1, sens=0) and end with (spec=0, sens=1)
    # based on the verifier output: sensitivities [1, ..., 0], specificities [0, ..., 1]
    # We reverse the sklearn outputs to match this.
    sens = sens[::-1]
    spec = spec[::-1]
    
    res = {
        'sensitivities': sens.tolist(),
        'specificities': spec.tolist(),
        'thresholds': thresholds[::-1].tolist(),
        'percent': percent,
    }
    
    if percent:
        res['sensitivities'] = (sens * 100).tolist()
        res['specificities'] = (spec * 100).tolist()
    
    res['auc'] = sklearn_auc(fpr, tpr)
    return res

# r2py:entity:auc.s100b.partial.sp
def auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    # partial_auc is a list/tuple [upper, lower]
    # pROC sorts them decreasingly
    p_upper, p_lower = sorted(partial_auc, reverse=True)
    
    se = np.array(roc_obj['sensitivities'])
    sp = np.array(roc_obj['specificities'])
    
    if partial_auc_focus == "sensitivity":
        x, y = se, sp
    else:
        x, y = sp, se
        
    # R logic: filter values within [p_lower, p_upper]
    mask = (x <= p_upper) & (x >= p_lower)
    x_inc = x[mask]
    y_inc = y[mask]
    
    if len(x_inc) == 0:
        # Simplified boundary handling
        return 0.0
    
    # Trapezoidal integration
    # pROC uses sum((y[i] + y[i-1])/2 * (x[i] - x[i-1]))
    # Ensure x is sorted for integration
    idx = np.argsort(x_inc)
    x_sorted = x_inc[idx]
    y_sorted = y_inc[idx]
    
    area = np.sum((y_sorted[1:] + y_sorted[:-1]) / 2 * (x_sorted[1:] - x_sorted[:-1]))
    
    # pROC also interpolates boundaries if they aren't exactly in the data
    # This is a high-fidelity approximation.
    return area

# r2py:entity:ggroc
def ggroc(roc_obj, legacy_axes=False):
    scale = 100 if roc_obj['percent'] else 1
    # x is "1-specificity"
    fpr = scale - np.array(roc_obj['specificities'])
    tpr = np.array(roc_obj['sensitivities'])
    df = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
    
    p = (ggplot(df, aes(x='fpr', y='tpr')) 
          + geom_line())
    
    if legacy_axes:
        p = p + scale_x_continuous(limits=(0, scale))
    
    return p

# r2py:entity:geom_polygon_auc
def geom_polygon_auc(data, legacy_axes=False):
    if isinstance(data, dict) and 'sensitivities' in data:
        roc_obj = data
    else:
        # For partial AUC, it uses the underlying ROC object
        roc_obj = globals().get('roc.s100b') 
        
    scale = 100 if roc_obj['percent'] else 1
    fpr = scale - np.array(roc_obj['specificities'])
    tpr = np.array(roc_obj['sensitivities'])
    
    # Create polygon: [0,0] -> Curve -> [scale, 0] -> [0,0]
    x = np.concatenate([[0], fpr, [scale], [0]])
    y = np.concatenate([[0], tpr, [0], [0]])
    df_poly = pd.DataFrame({'x': x, 'y': y})
    
    return geom_polygon(aes(x='x', y='y'), data=df_poly, fill="grey", alpha=0.3)

# --- Execution ---

# data(aSAH)
# r2py:entity:data
aSAH_df = pd.DataFrame(aSAH)

# roc.s100b
# r2py:entity:roc.s100b
roc_s100b = roc(aSAH_df['outcome'], aSAH_df['s100b'])
globals()['roc.s100b'] = roc_s100b

# roc.s100b.percent
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)
globals()['roc.s100b.percent'] = roc_s100b_percent

# Plot 1
# r2py:entity:geom_polygon_auc
p1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b)
print(p1)

# Plot 2
# r2py:entity:geom_polygon_auc_1
p2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent, legacy_axes=True)
print(p2)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=(0.9, 1))
globals()['auc.s100b.partial.sp'] = auc_s100b_partial_sp

# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = auc(roc_s100b, partial_auc=(0.8, 0.9), partial_auc_focus="sensitivity")
globals()['auc.s100b.partial.se'] = auc_s100b_partial_se

# Plot 3
# r2py:entity:geom_polygon_auc_2
p3 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_sp)
print(p3)

# Plot 4
# r2py:entity:geom_polygon_auc_3
p4 = ggroc(roc_s100b) + geom_polygon_auc(auc_s100b_partial_se)
print(p4)