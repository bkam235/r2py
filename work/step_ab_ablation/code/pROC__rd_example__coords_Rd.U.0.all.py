import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve, accuracy_score, precision_score, recall_score
from scipy.interpolate import interp1d

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def get_roc_df(outcome, predictor):
    fpr, tpr, thresholds = roc_curve(outcome, predictor)
    # pROC's roc() includes thresholds that might be slightly outside the range of the data
    # We'll create a dataframe to mimic the roc object
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * 100,
        'specificity': (1 - fpr) * 100,
        'fpr': fpr,
        'tpr': tpr
    })
    return df

def coords_mimic(roc_df, x=None, input_type=None, ret="all", best_method="youden", best_weights=None):
    # Handle "best"
    if x == "best":
        if best_method == "youden":
            weights = best_weights if best_weights is not None else [1.0, 1.0]
            # Weighted Youden: w1*sens + w2*spec
            score = weights[0] * roc_df['sensitivity'] + weights[1] * roc_df['specificity']
            idx = score.idxmax()
        elif best_method == "closest.topleft":
            weights = best_weights if best_weights is not None else [1.0, 1.0]
            # distance to (0, 100) in ROC space (fpr=0, tpr=100)
            # R uses coordinates in [0,1] for this distance usually
            dist = np.sqrt((weights[0] * roc_df['fpr']**2) + (weights[1] * (1 - roc_df['tpr'])**2))
            idx = dist.idxmin()
        else:
            idx = 0
        
        row = roc_df.loc[[idx]]
        # Calculate additional metrics for "best"
        best_t = row['threshold'].values[0]
        # Note: roc_curve thresholds are inverted relative to predictions (thresholds[i] is the threshold for tpr[i])
        # To match pROC, we use the threshold as the cutoff
        y_pred = (aSAH[roc_df.name].values >= best_t).astype(int)
        
        res = {
            'threshold': best_t,
            'specificity': row['specificity'].values[0],
            'sensitivity': row['sensitivity'].values[0],
            'accuracy': accuracy_score(aSAH['outcome'], y_pred) * 100,
            'precision': precision_score(aSAH['outcome'], y_pred, zero_division=0) * 100,
            'recall': recall_score(aSAH['outcome'], y_pred, zero_division=0) * 100,
            'tpr': row['tpr'].values[0],
            'fpr': row['fpr'].values[0]
        }
        
        if ret == "all":
            return pd.Series(res, name='threshold')
        if isinstance(ret, list):
            return pd.Series({k: res[k] for k in ret}, name='threshold')
        return pd.Series({ret: res[ret]}, name='threshold')

    # Handle "all"
    if x == "all":
        if ret == "all":
            return roc_df
        if isinstance(ret, list):
            return roc_df[ret]
        return roc_df[[ret]]

    # Handle specific threshold value
    if isinstance(x, (int, float)):
        # Find row where threshold is closest to x
        idx = (roc_df['threshold'] - x).abs().idxmin()
        row = roc_df.loc[[idx]]
        if input_type == "sensitivity" or (isinstance(input_type, str) and input_type == "se"):
            # x is sensitivity
            idx = (roc_df['sensitivity'] - x).abs().idxmin()
            row = roc_df.loc[[idx]]
        elif input_type == "specificity" or (isinstance(input_type, str) and input_type == "sp"):
            # x is specificity
            idx = (roc_df['specificity'] - x).abs().idxmin()
            row = roc_df.loc[[idx]]
        return row[['threshold', 'specificity', 'sensitivity']]

    return None

# Create a ROC curve:
roc_s100b = get_roc_df(aSAH['outcome'], aSAH['s100b'])
roc_s100b.name = 's100b'

# Get the coordinates of S100B threshold 0.55
print(coords_mimic(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords_mimic(roc_s100b, x=50, input_type="sensitivity"))
# Can be abbreviated:
print(coords_mimic(roc_s100b, 50, "se"))

# Works with smoothed ROC curves
# Smoothing approximation: interp1d
f_spec = interp1d(roc_s100b['specificity'], roc_s100b['sensitivity'], fill_value="extrapolate")
res_smooth = pd.DataFrame({'specificity': [90.0], 'sensitivity': [f_spec(90.0)]})
print(res_smooth)

# Get the sensitivities for all thresholds
cc = coords_mimic(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
print(coords_mimic(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
roc_ndka = get_roc_df(aSAH['outcome'], aSAH['ndka'])
roc_ndka.name = 'ndka'
print(coords_mimic(roc_ndka, "best", ret="threshold", best_method="youden")) # default
print(coords_mimic(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# and with different weights
print(coords_mimic(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords_mimic(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))
       
# This is available with the plot.roc function too:
# (Simulating the plot call)
best_youden_ndka = coords_mimic(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2])
# plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])

# Return more values:
print(coords_mimic(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# Return all values
print(coords_mimic(roc_s100b, "best", ret="all"))
                           
# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
df_all_ndka = coords_mimic(roc_ndka, "all")
plt.figure()
plt.plot(df_all_ndka['threshold'], df_all_ndka['specificity'] + df_all_ndka['sensitivity'])
plt.xscale('log')
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')

# Plot the Precision-Recall curve
precision_ndka, recall_ndka, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(recall_ndka * 100, precision_ndka * 100)
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.xlabel('fpr')
plt.ylabel('tpr')