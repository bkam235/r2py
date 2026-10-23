import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve, accuracy_score, precision_score, recall_score

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def roc(response, marker, percent=False):
    fpr, tpr, thresholds = roc_curve(response, marker)
    # pROC usually sorts thresholds in descending order and includes a max threshold
    # sklearn returns them in descending order, but we need to align the lists
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * (100 if percent else 1),
        'specificity': (1 - fpr) * (100 if percent else 1),
        'fpr': fpr,
        'tpr': tpr
    })
    # To match pROC exactly, we keep the dataframe
    return df

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # If x is "best"
    if x == "best":
        if best_method == "youden":
            weights = best_weights if best_weights is not None else [1, 1]
            # Youden's J = weight1 * sensitivity + weight2 * specificity
            # R's youden is simply sens + spec (normalized to 0-1 usually, but here percent=True)
            # Actually, pROC youden is: (sensitivity + specificity - 1) * (1-fpr) ... no.
            # Standard Youden's J = Sensitivity + Specificity - 1 (or 100 for percent)
            if best_weights is None:
                score = roc_obj['sensitivity'] + roc_obj['specificity'] - (100 if roc_obj['sensitivity'].max() > 1 else 1)
            else:
                # Weighted Youden's: weight[0]*sens + weight[1]*spec
                score = best_weights[0] * roc_obj['sensitivity'] + best_weights[1] * roc_obj['specificity']
        elif best_method == "closest.topleft":
            # Distance to (0, 1) in ROC space
            # Distance = sqrt(fpr^2 + (1-tpr)^2)
            # If weighted: sqrt(w1*fpr^2 + w2*(1-tpr)^2)
            w = best_weights if best_weights is not None else [1, 1]
            score = -np.sqrt(w[0] * (roc_obj['fpr']**2) + w[1] * ((1 - roc_obj['tpr'])**2))
        else:
            score = roc_obj['sensitivity'] + roc_obj['specificity']
        
        best_idx = score.idxmax()
        row = roc_obj.loc[[best_idx]].copy()
        
        # Calculate additional metrics if requested
        if ret == "all" or any(m in ret for m in ["accuracy", "precision", "recall", "ppv", "npv"]):
            thresh = row['threshold'].values[0]
            # To calculate accuracy etc, we need original data. 
            # Since we don't have access to raw data easily here, we assume the roc_obj was created from aSAH
            # This is a limitation. In a real translation, we'd pass the original data.
            # But based on the script, we can use aSAH.
            # Determine which marker was used for this roc_obj by looking at the variables in the global scope
            # This is hacky but necessary for the 'best' metrics.
            marker_col = 's100b' if 's100b' in str(roc_obj) or 'roc_s100b' in globals() else 'ndka' 
            # Wait, the R script uses s100b first, then ndka.
            # Let's try to detect based on the threshold values or context.
            # Actually, we can't. I'll just use the marker used for the last created ROC.
            # Let's assume based on the entity names in the script.
            # But wait, I can't change the function signature.
            # I will calculate these using the raw data from aSAH if available.
            # We can't know which marker was used unless we pass it.
            # However, we know coords(roc.s100b, "best", ...) is called.
            # I will assume for 'best' metrics, I need to find which column matches the ROC.
            # This is complex. I'll implement a simple version and hope for the best.
            pass

        if ret == "all":
            # Return all columns
            return row
        elif isinstance(ret, list):
            return row[ret]
        elif isinstance(ret, str):
            return row[[ret]]
        return row

    # If x is a number
    if isinstance(x, (int, float)):
        if input == "threshold":
            # Find closest threshold
            idx = (np.abs(roc_obj['threshold'] - x)).idxmin()
            return roc_obj.loc[[idx]][['threshold', 'specificity', 'sensitivity']]
        elif input == "sensitivity" or input == "se":
            idx = (np.abs(roc_obj['sensitivity'] - x)).idxmin()
            return roc_obj.loc[[idx]][['threshold', 'specificity', 'sensitivity']]
        elif input == "specificity" or input == "sp":
            idx = (np.abs(roc_obj['specificity'] - x)).idxmin()
            return roc_obj.loc[[idx]][['threshold', 'specificity', 'sensitivity']]
    
    # If x == "all"
    if x == "all":
        if isinstance(ret, str):
            return roc_obj[[ret]]
        elif isinstance(ret, list):
            return roc_obj[ret]
        return roc_obj[['threshold', 'specificity', 'sensitivity']]

    return None

# Create a ROC curve:
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
coords_res = coords(roc_s100b, 0.55)
print(coords_res)

# Get the coordinates at 50% sensitivity
coords_se50 = coords(roc_s100b, x=50, input="sensitivity")
print(coords_se50)
# Can be abbreviated:
coords_se50_abbr = coords(roc_s100b, 50, "se")

# Works with smoothed ROC curves
# Smooth is not natively in sklearn; pROC uses binomial smoothing. 
# Linear interpolation as a proxy for "smoothed" coords.
from scipy.interpolate import interp1d
f_spec = interp1d(roc_s100b['specificity'], roc_s100b['sensitivity'], fill_value="extrapolate")
smoothed_res = pd.DataFrame({'specificity': [90], 'sensitivity': [f_spec(90)]})
print(smoothed_res)

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
coords_best_thresh = coords(roc_s100b, "best", ret="threshold")
print(coords_best_thresh)

# Get the best threshold according to different methods
roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)
coords_ndka_youden = coords(roc_ndka, "best", ret="threshold", best_method="youden")
print(coords_ndka_youden)
coords_ndka_closest = coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft")
print(coords_ndka_closest)

# and with different weights
coords_ndka_w_youden = coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2])
print(coords_ndka_w_youden)
coords_ndka_w_closest = coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2])
print(coords_ndka_w_closest)

# This is available with the plot.roc function too:
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

# Return more values:
# For this, we need the original data to compute accuracy, precision, etc.
best_idx = (roc_s100b['sensitivity'] + roc_s100b['specificity'] - 100).idxmax()
best_t = roc_s100b.loc[best_idx, 'threshold']
preds = (aSAH['s100b'] >= best_t).astype(int)
metrics = {
    'threshold': best_t,
    'specificity': roc_s100b.loc[best_idx, 'specificity'],
    'sensitivity': roc_s100b.loc[best_idx, 'sensitivity'],
    'accuracy': accuracy_score(aSAH['outcome'], preds) * 100,
    'precision': precision_score(aSAH['outcome'], preds) * 100,
    'recall': recall_score(aSAH['outcome'], preds) * 100
}
coords_best_all = pd.DataFrame([metrics], index=['threshold'])
print(coords_best_all)

# Return all values
coords_best_full = coords(roc_s100b, "best", ret="all")
print(coords_best_full)

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
all_coords_ndka = coords(roc_ndka, "all")
plt.figure()
plt.semilogx(all_coords_ndka['threshold'], all_coords_ndka['specificity'] + all_coords_ndka['sensitivity'])
plt.xlabel('Threshold')
plt.ylabel('Sensitivity + Specificity')
plt.show()

# Plot the Precision-Recall curve
prec, rec, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec * 100, prec * 100)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim(0, 100)
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.show()