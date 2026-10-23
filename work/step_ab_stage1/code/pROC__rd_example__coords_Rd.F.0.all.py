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
    # pROC usually handles thresholds by including the max value
    # sklearn's thresholds are sorted descending
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * (100 if percent else 1),
        'specificity': (1 - fpr) * (100 if percent else 1)
    })
    # pROC typically sorts by threshold ascending or maintains specific order
    # We store it as a object to mimic the 'roc' class
    return df

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    df = roc_obj.copy()
    
    # Calculate derived metrics for "all" or "best"
    # Sensitivity (TPR) and Specificity (TNR) are already there
    # Accuracy = (TP + TN) / (TP + TN + FP + FN)
    # Since we only have the curve, we need the original data to calculate accuracy/precision/recall for a threshold
    # But for the sake of this translation, we'll calculate them if needed.
    
    if x == "best":
        if best_method == "youden":
            weights = best_weights if best_weights is not None else [1, 1]
            # Youden J = weight1*sens + weight2*spec
            # pROC's youden is usually sens + spec - 1 (or 100)
            # With weights: w1 * sens + w2 * spec
            score = weights[0] * df['sensitivity'] + weights[1] * df['specificity']
            idx = score.idxmax()
        elif best_method == "closest.topleft":
            weights = best_weights if best_weights is not None else [1, 1]
            # Distance to (0, 1) in ROC space: sqrt( (w1*fpr)^2 + (w2*(1-tpr))^2 )
            # Convert to 0-1 scale for distance calculation
            sens = df['sensitivity'] / 100 if df['sensitivity'].max() > 1 else df['sensitivity']
            spec = df['specificity'] / 100 if df['specificity'].max() > 1 else df['specificity']
            dist = np.sqrt((weights[0] * (1 - spec))**2 + (weights[1] * (1 - sens))**2)
            idx = dist.idxmin()
        else:
            idx = 0
        
        row = df.loc[[idx]]
    elif x is not None:
        if input == "threshold":
            # Find closest threshold
            idx = (df['threshold'] - x).abs().idxmin()
            row = df.loc[[idx]]
        elif input in ["sensitivity", "se"]:
            idx = (df['sensitivity'] - x).abs().idxmin()
            row = df.loc[[idx]]
        elif input in ["specificity", "sp"]:
            idx = (df['specificity'] - x).abs().idxmin()
            row = df.loc[[idx]]
        else:
            row = df
    else:
        row = df

    # Handle 'ret'
    if ret == "all":
        # In a real pROC, "all" returns a huge dataframe of all possible metrics
        # We'll provide the core ones available in our df
        res = row.copy()
    elif isinstance(ret, list):
        res = row[ret] if all(c in row.columns for c in ret) else row
    elif isinstance(ret, str):
        res = row[[ret]] if ret in row.columns else row
    else:
        res = row

    return res

# Create a ROC curve:
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
print(coords(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords(roc=roc_s100b, x=50, input="sensitivity"))
# Can be abbreviated:
print(coords(roc_s100b, 50, "se"))

# Works with smoothed ROC curves (Approximate with original for this example)
print(coords(roc_s100b, 90, "specificity"))

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# and with different weights
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# plot(roc.ndka, ...) - Mocking the plot call
plt.figure()
plt.plot(1-roc_ndka['specificity']/100, roc_ndka['sensitivity']/100)
plt.title("ROC Curve ndka")
plt.show()

# Return more values:
# For accuracy/precision/recall, we need to compute them for the 'best' threshold
best_row = coords(roc_s100b, "best", ret="all")
best_t = best_row['threshold'].values[0]
preds = (aSAH['s100b'] >= best_t).astype(int)
acc = accuracy_score(aSAH['outcome'], preds) * 100
prec = precision_score(aSAH['outcome'], preds) * 100
rec = recall_score(aSAH['outcome'], preds) * 100

# Combine into a dataframe to mimic the coords output
result_best = best_row.copy()
result_best['accuracy'] = acc
result_best['precision'] = prec
result_best['recall'] = rec
print(result_best[['threshold', 'specificity', 'sensitivity', 'accuracy', 'precision', 'recall']])

# Return all values
print(coords(roc_s100b, "best", ret="all"))

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
plot_data_all = coords(roc_ndka, "all")
plt.figure()
plt.semilogx(plot_data_all['threshold'], plot_data_all['specificity'] + plot_data_all['sensitivity'])
plt.xlabel("threshold")
plt.ylabel("specificity + sensitivity")
plt.show()

# Plot the Precision-Recall curve
prec_pr, rec_pr, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec_pr * 100, prec_pr * 100)
plt.xlabel("recall")
plt.ylabel("precision")
plt.ylim(0, 100)
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
plt.figure()
plt.plot(1 - roc_ndka['specificity']/100, roc_ndka['sensitivity']/100)
plt.xlabel("fpr")
plt.ylabel("tpr")
plt.show()