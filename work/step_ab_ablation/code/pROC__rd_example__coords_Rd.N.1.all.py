# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 22

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve

class ROC:
    def __init__(self, response, marker, percent=False):
        self.response = np.array(response)
        self.marker = np.array(marker)
        self.percent = percent
        
        # pROC determines direction automatically
        # If marker increases, sensitivity increases (case > control)
        # sklearn.roc_curve expects this.
        fpr, tpr, thresholds = roc_curve(self.response, self.marker)
        
        # pROC's thresholds are slightly different (unique values of the marker)
        # and usually ordered from highest to lowest.
        self.tpr = tpr
        self.fpr = fpr
        self.thresholds = thresholds
        
        self.sensitivity = tpr * (100 if percent else 1)
        self.specificity = (1 - fpr) * (100 if percent else 1)

    def smooth(self):
        # pROC smooth() uses binomial smoothing. 
        # For this example's purpose, we return a proxy or the object itself.
        return self

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # Calculate all metrics for all thresholds
    res = pd.DataFrame({
        'threshold': roc_obj.thresholds,
        'sensitivity': roc_obj.sensitivity,
        'specificity': roc_obj.specificity,
        'tpr': roc_obj.tpr * (100 if roc_obj.percent else 1),
        'fpr': roc_obj.fpr * (100 if roc_obj.percent else 1)
    })
    
    # Calculate accuracy, precision, recall
    # We need to calculate these based on the actual data for each threshold
    # to be accurate, but for 'all' it's computationally heavy.
    # pROC calculates these on the fly.
    
    if x == "best":
        if best_method == "youden":
            # Youden's J = Sens + Spec - 100 (or 1)
            offset = 100 if roc_obj.percent else 1
            if best_weights is not None:
                # weights[0]*sens + weights[1]*spec
                score = best_weights[0] * res['sensitivity'] + best_weights[1] * res['specificity']
            else:
                score = res['sensitivity'] + res['specificity'] - offset
            idx = score.idxmax()
        elif best_method == "closest.topleft":
            # Distance to (0, 100) or (0, 1)
            # R's closest.topleft uses a specific distance formula
            # distance = sqrt( (spec-1)^2 + (sens-1)^2 ) approx
            # scaled by weights if provided
            w_sens = best_weights[0] if best_weights is not None else 1
            w_spec = best_weights[1] if best_weights is not None else 1
            
            # Normalize to 0-1 for distance calculation
            s_norm = res['sensitivity'] / (100 if roc_obj.percent else 1)
            sp_norm = res['specificity'] / (100 if roc_obj.percent else 1)
            dist = np.sqrt(w_spec * (1 - sp_norm)**2 + w_sens * (1 - s_norm)**2)
            idx = dist.idxmin()
        
        row = res.iloc[[idx]].copy()
        
        # Calculate Precision/Recall/Accuracy for the 'best' threshold
        t = row['threshold'].values[0]
        preds = (roc_obj.marker >= t).astype(int)
        tp = np.sum((preds == 1) & (roc_obj.response == 1))
        fp = np.sum((preds == 1) & (roc_obj.response == 0))
        tn = np.sum((preds == 0) & (roc_obj.response == 0))
        fn = np.sum((preds == 0) & (roc_obj.response == 1))
        
        acc = (tp + tn) / len(preds)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        mult = 100 if roc_obj.percent else 1
        row['accuracy'] = acc * mult
        row['precision'] = prec * mult
        row['recall'] = rec * mult
        
        if ret != "all":
            if isinstance(ret, list):
                return row[ret]
            return row[ret].values[0]
        return row

    elif x is not None:
        if input == "threshold":
            # find row where threshold is closest to x
            idx = (res['threshold'] - x).abs().idxmin()
            row = res.iloc[[idx]]
        elif input == "sensitivity" or input == "se":
            idx = (res['sensitivity'] - x).abs().idxmin()
            row = res.iloc[[idx]]
        elif input == "specificity" or input == "sp":
            idx = (res['specificity'] - x).abs().idxmin()
            row = res.iloc[[idx]]
        else:
            row = res
            
        if ret != "all":
            if isinstance(ret, list):
                return row[ret]
            return row[ret].values[0] if ret in row.columns else row
        return row
    
    else: # x is None, "all"
        if ret != "all":
            if isinstance(ret, list):
                return res[ret]
            return res[ret]
        return res

# Create a ROC curve:
roc_s100b = ROC(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
print(coords(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords(roc=roc_s100b, x=50, input="sensitivity"))
# Can be abbreviated:
print(coords(roc_s100b, 50, "se"))

# Works with smoothed ROC curves
print(coords(roc_s100b.smooth(), 90, "specificity"))

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc.values if hasattr(cc, 'values') else cc)

# Get the best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
roc_ndka = ROC(aSAH['outcome'], aSAH['ndka'], percent=True)
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="youden")) # default
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="closest.topleft"))

# and with different weights
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="closest.topleft", best_weights=[5, 0.2]))
       
# This is available with the plot.roc function too:
# (Plotting logic skipped as it's a visual output, but logic matches coords)

# Return more values:
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy",
                           "precision", "recall"]))

# Return all values
print(coords(roc_s100b, "best", ret = "all"))
                           
# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
c_all_ndka = coords(roc_ndka, "all")
plt.figure()
plt.semilogx(c_all_ndka['threshold'], c_all_ndka['specificity'] + c_all_ndka['sensitivity'])
plt.show()

# Plot the Precision-Recall curve
c_pr_ndka = coords(roc_ndka, "all", ret = ["recall", "precision"])
# Note: 'all' for recall/precision needs actual calculation
# Re-calculating precision/recall for all thresholds
precisions, recalls, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(recalls * 100, precisions * 100)
plt.ylim(0, 100)
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
c_tpr_fpr = coords(roc_ndka, "all", ret = ["tpr", "fpr"])
plt.figure()
plt.plot(c_tpr_fpr['fpr'], c_tpr_fpr['tpr'])
plt.show()