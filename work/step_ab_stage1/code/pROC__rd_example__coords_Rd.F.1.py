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

def get_roc_df(y_true, y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    # pROC stores roc objects with specific sensitivities and specificities.
    # percent=TRUE means values are 0-100.
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * 100,
        'specificity': (1 - fpr) * 100,
        'tpr': tpr * 100,
        'fpr': fpr * 100
    })
    return df

def coords(roc_df, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # Support "best"
    if x == "best":
        if best_method == "youden":
            weights = best_weights if best_weights is not None else [1, 1]
            # Weighted Youden's index: w1*sens + w2*spec
            scores = weights[0] * roc_df['sensitivity'] + weights[1] * roc_df['specificity']
            idx = scores.idxmax()
        elif best_method == "closest.topleft":
            weights = best_weights if best_weights is not None else [1, 1]
            # Distance to (0, 100) in ROC space: sqrt(w1*fpr^2 + w2*(100-tpr)^2)
            # Note: pROC's closest.topleft uses scaled distance.
            dist = np.sqrt(weights[0] * (roc_df['fpr']**2) + weights[1] * ((100 - roc_df['tpr'])**2))
            idx = dist.idxmin()
        else:
            idx = 0
        row = roc_df.loc[idx]
    elif input == "threshold":
        # Find row where threshold is closest to x
        idx = (roc_df['threshold'] - x).abs().idxmin()
        row = roc_df.loc[idx]
    elif input in ["sensitivity", "se"]:
        idx = (roc_df['sensitivity'] - x).abs().idxmin()
        row = roc_df.loc[idx]
    elif input in ["specificity", "sp"]:
        idx = (roc_df['specificity'] - x).abs().idxmin()
        row = roc_df.loc[idx]
    elif x == "all":
        if ret == "all": return roc_df
        if isinstance(ret, list): return roc_df[ret]
        return roc_df[[ret]] if ret in roc_df.columns else roc_df
    else:
        return None

    if ret == "all":
        return row
    if isinstance(ret, list):
        # Calculate accuracy, precision, recall if requested for "best"
        res = row.to_dict()
        if "accuracy" in ret or "precision" in ret or "recall" in ret:
            t = row['threshold']
            preds = (aSAH['s100b'] if 's100b' in locals() else aSAH['ndka']) >= t
            res['accuracy'] = accuracy_score(aSAH['outcome'], preds) * 100
            res['precision'] = precision_score(aSAH['outcome'], preds) * 100
            res['recall'] = recall_score(aSAH['outcome'], preds) * 100
        return pd.Series({k: res[k] for k in ret if k in res})
    
    return pd.Series({ret: row[ret]}) if ret in row else row

# Create ROC curves
roc_s100b = get_roc_df(aSAH['outcome'], aSAH['s100b'])
roc_ndka = get_roc_df(aSAH['outcome'], aSAH['ndka'])

# Get the coordinates of S100B threshold 0.55
print(coords(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords(roc_s100b, x=50, input="sensitivity"))
print(coords(roc_s100b, 50, "se"))

# Works with smoothed ROC curves (linear interpolation approximation)
f_interp = interp1d(roc_s100b['specificity'], roc_s100b['threshold'], fill_value="extrapolate")
print(f_interp(90))

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# Weights
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# Return more values
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))
print(coords(roc_s100b, "best", ret="all"))

# Plot 1: specificity + sensitivity vs. threshold
plot_data_1 = coords(roc_ndka, "all")
plt.figure()
plt.semilogx(plot_data_1['threshold'], plot_data_1['specificity'] + plot_data_1['sensitivity'])
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# Plot 2: Precision-Recall curve
prec, rec, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec * 100, prec * 100)
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# Plot 3: TPR vs FPR
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()

# Plot 4: ROC curve (mimicking plot(roc.ndka, ...))
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.xlabel('Specificity')
plt.ylabel('Sensitivity')
plt.show()