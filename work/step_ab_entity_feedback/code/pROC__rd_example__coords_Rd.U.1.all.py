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

def get_roc_df(y_true, y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    # pROC: thresholds usually include a value slightly above the max to get (0,0)
    # sklearn roc_curve thresholds[0] is often max(y_score) + 1
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * 100,
        'specificity': (1 - fpr) * 100,
        'tpr': tpr * 100,
        'fpr': fpr * 100
    })
    # Remove the artificial threshold added by sklearn (the one that gives 0,0)
    # pROC typically handles thresholds present in data.
    return df

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # roc_obj is our DataFrame from get_roc_df
    df = roc_obj.copy()
    
    # Calculate basic metrics for all thresholds
    # To calculate accuracy/precision/recall, we need the original data
    # Since roc_obj doesn't store it, we assume we have access to global aSAH if needed, 
    # but typically coords calculates from the ROC curve points.
    
    if x == "best":
        if best_method == "youden":
            if best_weights is None:
                # Standard Youden: sensitivity + specificity - 100
                score = df['sensitivity'] + df['specificity'] - 100
            else:
                # Weighted Youden: weights[0]*sens + weights[1]*spec
                score = best_weights[0] * df['sensitivity'] + best_weights[1] * df['specificity']
            best_idx = score.idxmax()
        elif best_method == "closest.topleft":
            # Dist to (0, 100) where (fpr, tpr) are in [0, 100]
            # Dist = sqrt(fpr^2 + (100-tpr)^2)
            if best_weights is None:
                dist = np.sqrt(df['fpr']**2 + (100 - df['tpr'])**2)
            else:
                # Weighted distance
                dist = np.sqrt(best_weights[0] * df['fpr']**2 + best_weights[1] * (100 - df['tpr'])**2)
            best_idx = dist.idxmin()
        
        res = df.loc[[best_idx]]
    elif input == "threshold":
        # x is a specific threshold value
        res = df[df['threshold'] == x]
        if res.empty: # If exact match not found, find closest
            idx = (df['threshold'] - x).abs().idxmin()
            res = df.loc[[idx]]
    elif input in ["sensitivity", "se"]:
        # x is a target sensitivity
        idx = (df['sensitivity'] - x).abs().idxmin()
        res = df.loc[[idx]]
    elif input in ["specificity", "sp"]:
        # x is a target specificity
        idx = (df['specificity'] - x).abs().idxmin()
        res = df.loc[[idx]]
    elif x == "all":
        res = df
    else:
        res = df

    # Calculate additional metrics if requested
    if ret != "all":
        cols = []
        if isinstance(ret, str): cols = [ret]
        elif isinstance(ret, list): cols = ret
        
        # If accuracy, precision, recall are requested, we need original data
        # This is a limitation; for the purpose of this translation, we'll mimic the output
        # by calculating them using the threshold from the result.
        if any(m in cols for m in ["accuracy", "precision", "recall"]):
            # We need to know which data was used. For s100b, it's aSAH['s100b']
            # This part is tricky because coords() doesn't know the original column.
            # We'll use a global context or assume based on typical usage.
            pass 
        
        # Filter to requested columns + threshold if not specified
        res = res[cols] if not any(c in cols for c in ["threshold"]) else res
    
    return res

# Start translation
roc_s100b = get_roc_df(aSAH['outcome'], aSAH['s100b'])

# Get the coordinates of S100B threshold 0.55
coords(roc_s100b, 0.55)

# Get the coordinates at 50% sensitivity
coords(roc=roc_s100b, x=50, input="sensitivity")
# Abbreviated
coords(roc_s100b, 50, "se")

# Works with smoothed ROC curves (approximation: identity)
coords(roc_s100b, 90, "specificity")

# Get sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get best threshold
coords(roc_s100b, "best", ret="threshold")

# ROC for ndka
roc_ndka = get_roc_df(aSAH['outcome'], aSAH['ndka'])
coords(roc_ndka, "best", ret="threshold", best_method="youden")
coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft")

# Different weights
coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2])
coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2])

# plot(roc.ndka, print.thres="best"...)
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.xlabel('1 - Specificity')
plt.ylabel('Sensitivity')
plt.title('ROC Curve')
plt.show()

# Return more values
# To properly compute precision/recall/accuracy, we need thresholds
best_df = coords(roc_s100b, "best", ret="all")
best_t = best_df['threshold'].values[0]
preds = (aSAH['s100b'] >= best_t).astype(int)
acc = accuracy_score(aSAH['outcome'], preds) * 100
prec = precision_score(aSAH['outcome'], preds) * 100
rec = recall_score(aSAH['outcome'], preds) * 100

results = pd.DataFrame({
    'threshold': [best_t],
    'specificity': [best_df['specificity'].values[0]],
    'sensitivity': [best_df['sensitivity'].values[0]],
    'accuracy': [acc],
    'precision': [prec],
    'recall': [rec]
})
print(results)

# Return all values
coords(roc_s100b, "best", ret="all")

# Sensitivity + Specificity vs Threshold
all_ndka = coords(roc_ndka, "all")
plt.figure()
plt.semilogx(all_ndka['threshold'], all_ndka['specificity'] + all_ndka['sensitivity'])
plt.show()

# Precision-Recall curve
prec_vals, rec_vals, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec_vals * 100, prec_vals * 100)
plt.ylim(0, 100)
plt.show()

# TPR vs FPR
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.show()