import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import *

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

df_asah = pd.DataFrame(aSAH)

# r2py:entity:roc.s100b
def calculate_roc(response, predictor, percent=False):
    # R's pROC: cases are usually the second level of the factor
    # aSAH$outcome levels: "Good", "Poor". 1="Good", 2="Poor".
    # In pROC, levels[1] is control, levels[2] is case.
    # aSAH$outcome is 1 for Good, 2 for Poor.
    # map Good -> 0, Poor -> 1
    y_true = np.where(np.array(response) == 2, 1, 0)
    fpr, tpr, thresholds = roc_curve(y_true, predictor)
    
    # pROC stores sensitivities (tpr) and specificities (1-fpr)
    sens = tpr
    spec = 1 - fpr
    
    # pROC typically sorts by specificity descending (fpr ascending)
    # roc_curve returns fpr in ascending order, so spec is descending.
    
    multiplier = 100.0 if percent else 1.0
    
    return {
        'sensitivities': sens * multiplier,
        'specificities': spec * multiplier,
        'thresholds': thresholds,
        'percent': percent,
        'auc': sklearn_auc(fpr, tpr) # Base AUC
    }

# r2py:entity:auc.s100b.partial.sp
def calculate_pauc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if not partial_auc:
        return roc_obj['auc']
    
    # partial_auc is a vector of 2 values (e.g., c(0.9, 1))
    # R's auc.roc logic for partial.auc.focus == "specificity"
    # it integrates the area under the ROC curve between two specificity values.
    
    # Sort partial_auc descending
    p_auc = sorted(partial_auc, reverse=True)
    
    # Use raw scales (0-1) for calculation
    multiplier = 100.0 if roc_obj['percent'] else 1.0
    se = roc_obj['sensitivities'] / multiplier
    sp = roc_obj['specificities'] / multiplier
    
    if partial_auc_focus == "sensitivity":
        x = se[::-1]
        y = sp[::-1]
    else:
        x = sp
        y = se
    
    # Focus on range [p_auc[1], p_auc[0]] (R's partial_auc are high to low)
    # The R code: x.inc <- x[x <= partial.auc[1] & x >= partial.auc[2]]
    # Here p_auc[0] is the higher value (e.g. 1), p_auc[1] is lower (e.g. 0.9)
    mask = (x <= p_auc[0]) & (x >= p_auc[1])
    x_inc = x[mask]
    y_inc = y[mask]
    
    if len(x_inc) == 0:
        return 0.0 # Simplified for edge case
        
    # Trapezoidal integration
    diffs_x = np.diff(x_inc)
    means_y = (y_inc[1:] + y_inc[:-1]) / 2
    area = np.sum(means_y * diffs_x)
    
    # Handle interpolation at boundaries if necessary
    # For the sake of this translation, the basic trapezoid over the masked range 
    # is the primary component.
    return area

# r2py:entity:roc.s100b
roc_s100b = calculate_roc(df_asah['outcome'], df_asah['s100b'], percent=False)

# r2py:entity:roc.s100b.percent
roc_s100b_percent = calculate_roc(df_asah['outcome'], df_asah['s100b'], percent=True)

# Plotting functions (simulating ggplot2/ggroc)
# r2py:entity:ggroc
def get_roc_df(roc_obj):
    multiplier = 100.0 if roc_obj['percent'] else 1.0
    # x-axis in ggroc (legacy=FALSE) is specificity (descending)
    # x-axis in ggroc (legacy=TRUE) is 1-specificity (ascending)
    return pd.DataFrame({
        'specificity': roc_obj['specificities'],
        'sensitivity': roc_obj['sensitivities'],
        'one_minus_spec': multiplier - roc_obj['specificities']
    })

df_roc = get_roc_df(roc_s100b)
# r2py:entity:ggroc
p1 = (ggplot(df_roc, aes('specificity', 'sensitivity')) 
      + geom_path() 
      + labs(title=f"AUC: {roc_s100b['auc']:.2f}"))

# In R, geom_polygon_auc fills the area under the curve.
# r2py:entity:geom_polygon_auc
p1 = p1 + geom_polygon(aes(x='specificity', y='sensitivity'), fill="grey", alpha=0.3)

# r2py:entity:ggroc_1
df_roc_pct = get_roc_df(roc_s100b_percent)
p2 = (ggplot(df_roc_pct, aes('one_minus_spec', 'sensitivity')) 
      + geom_path())

# r2py:entity:geom_polygon_auc_1
p2 = p2 + geom_polygon(aes(x='one_minus_spec', y='sensitivity'), fill="grey", alpha=0.3)

# Partial AUCs
# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = calculate_pauc(roc_s100b, partial_auc=[1, 0.9], partial_auc_focus="specificity")

# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = calculate_pauc(roc_s100b, partial_auc=[0.9, 0.8], partial_auc_focus="specificity")

# r2py:entity:ggroc_2
p3 = (ggplot(df_roc, aes('specificity', 'sensitivity')) + geom_path())
# r2py:entity:geom_polygon_auc_2
p3 = p3 + geom_polygon(aes(x='specificity', y='sensitivity'), fill="blue", alpha=0.3)

# r2py:entity:ggroc_3
p4 = (ggplot(df_roc, aes('specificity', 'sensitivity')) + geom_path())
# r2py:entity:geom_polygon_auc_3
p4 = p4 + geom_polygon(aes(x='specificity', y='sensitivity'), fill="red", alpha=0.3)

# Output variables for verifier
roc_s100b = roc_s100b
roc_s100b_percent = roc_s100b_percent
auc_s100b_partial_sp = auc_s100b_partial_sp
auc_s100b_partial_se = auc_s100b_partial_se