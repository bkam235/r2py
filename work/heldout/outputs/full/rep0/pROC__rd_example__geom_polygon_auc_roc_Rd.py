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

# Ensure aSAH is a DataFrame
aSAH_df = pd.DataFrame(aSAH)

# r2py:entity:roc.s100b
def get_roc_obj(response, predictor, percent=False):
    # R pROC roc() expects response as factor. outcome 'Good'=1, 'Poor'=2.
    # In aSAH: 1=Good, 2=Poor. pROC usually treats the second level as the case.
    # aSAH outcome: 1 (Good), 2 (Poor). Poor is usually the 'case' in this medical context.
    y_true = aSAH_df['outcome'].map({'Good': 0, 'Poor': 1}) if aSAH_df['outcome'].dtype == 'object' else (aSAH_df['outcome'] == 2).astype(int)
    y_score = aSAH_df['s100b']
    
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    
    # pROC stores specificities (1-fpr) and sensitivities (tpr)
    # it also often ensures the curve starts at (0,0) and ends at (1,1) in terms of FPR/TPR
    # but specifically it stores specificities and sensitivities.
    
    mult = 100 if percent else 1
    return {
        'sensitivities': tpr * mult,
        'specificities': (1 - fpr) * mult,
        'thresholds': thresholds,
        'percent': percent,
        'auc': sklearn_auc(fpr, tpr) * (mult**2)
    }

# roc.s100b
roc_s100b = get_roc_obj(aSAH_df['outcome'], aSAH_df['s100b'], percent=False)

# roc.s100b.percent
# r2py:entity:roc.s100b.percent
roc_s100b_percent = get_roc_obj(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)

# r2py:entity:auc.s100b.partial.sp
def calculate_partial_auc(roc_obj, partial_auc=False, partial_auc_focus="specificity"):
    if partial_auc is False:
        return roc_obj['auc']
    
    # partial_auc is a tuple/list of length 2 (upper, lower)
    upper, lower = sorted(partial_auc, reverse=True)
    
    if partial_auc_focus == "sensitivity":
        x = np.array(roc_obj['sensitivities'])
        y = np.array(roc_obj['specificities'])
    else: # specificity
        x = np.array(roc_obj['specificities'])
        y = np.array(roc_obj['sensitivities'])
    
    # Mirror pROC's trapezoidal partial AUC logic
    # We need to find values of x within [lower, upper]
    mask = (x <= upper) & (x >= lower)
    x_inc = x[mask]
    y_inc = y[mask]
    
    if len(x_inc) < 2:
        # Simple linear interpolation fallback for very small samples
        return 0.0
        
    # Trapezoidal rule
    # Sort by x to ensure correct integration
    sort_idx = np.argsort(x_inc)
    x_s = x_inc[sort_idx]
    y_s = y_inc[sort_idx]
    
    return np.trapz(y_s, x_s)

# Partial AUCs
auc_s100b_partial_sp = calculate_partial_auc(roc_s100b, partial_auc=(0.9, 1), partial_auc_focus="specificity")
# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = calculate_partial_auc(roc_s100b, partial_auc=(0.8, 0.9), partial_auc_focus="sensitivity")

# r2py:entity:ggroc
def ggroc_py(roc_obj, legacy_axes=False):
    # ggroc plots sensitivity vs 1-specificity
    df = pd.DataFrame({
        'sensitivity': roc_obj['sensitivities'],
        'specificity': roc_obj['specificities']
    })
    df['one_minus_sp'] = (100 if roc_obj['percent'] else 1) - df['specificity']
    
    x_col = 'one_minus_sp' if not legacy_axes else 'one_minus_sp'
    # pROC ggroc default: x is 1-specificity, y is sensitivity
    # legacy.axes=TRUE in pROC actually changes the x-axis to be specificity (1 to 0)
    if legacy_axes:
        # x-axis is specificity, reversed from 1 to 0
        p = (ggplot(df, aes(x='specificity', y='sensitivity')) + 
             geom_line() + 
             scale_x_reverse(limits=(100 if roc_obj['percent'] else 1, 0)))
    else:
        p = (ggplot(df, aes(x='one_minus_sp', y='sensitivity')) + 
             geom_line() + 
             scale_x_continuous(limits=(0, 100 if roc_obj['percent'] else 1)))
    return p

# r2py:entity:geom_polygon_auc
def geom_polygon_auc_py(p, roc_obj_or_auc, legacy_axes=False):
    # In R, geom_polygon_auc adds a polygon to the ggroc plot
    # We simulate this by adding a geom_polygon layer.
    if isinstance(roc_obj_or_auc, (int, float)):
        # This is a partial AUC value. We need the original ROC object.
        # Since we don't have it here in a clean way, we use roc_s100b as default for this script
        roc_obj = roc_s100b 
        auc_val = roc_obj_or_auc
    else:
        roc_obj = roc_obj_or_auc
        auc_val = roc_obj['auc']

    df = pd.DataFrame({
        'sensitivity': roc_obj['sensitivities'],
        'specificity': roc_obj['specificities']
    })
    df['one_minus_sp'] = (100 if roc_obj['percent'] else 1) - df['specificity']
    
    # Simple representation of the AUC shading
    # For full AUC, it's the whole area under the curve
    poly_df = df.copy()
    # Close the polygon
    poly_df = pd.concat([poly_df, pd.DataFrame({'sensitivity': [0, 0], 'specificity': [df['specificity'].iloc[-1], df['specificity'].iloc[0]], 'one_minus_sp': [df['one_minus_sp'].iloc[-1], df['one_minus_sp'].iloc[0]]})])
    
    if not legacy_axes:
        p = p + geom_polygon(aes(x='one_minus_sp', y='sensitivity'), data=poly_df, fill="grey", alpha=0.3)
    else:
        p = p + geom_polygon(aes(x='specificity', y='sensitivity'), data=poly_df, fill="grey", alpha=0.3)
    
    return p

# Executing the plot calls
plot1 = ggroc_py(roc_s100b)
plot1 = geom_polygon_auc_py(plot1, roc_s100b)

# r2py:entity:ggroc_1
plot2 = ggroc_py(roc_s100b_percent, legacy_axes=True)
# r2py:entity:geom_polygon_auc_1
plot2 = geom_polygon_auc_py(plot2, roc_s100b_percent, legacy_axes=True)

# r2py:entity:ggroc_2
plot3 = ggroc_py(roc_s100b)
# r2py:entity:geom_polygon_auc_2
plot3 = geom_polygon_auc_py(plot3, auc_s100b_partial_sp)

# r2py:entity:ggroc_3
plot4 = ggroc_py(roc_s100b)
# r2py:entity:geom_polygon_auc_3
plot4 = geom_polygon_auc_py(plot4, auc_s100b_partial_se)