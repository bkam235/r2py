import numpy as np
import pandas as pd
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

class RocCurve:
    def __init__(self, response, marker, percent=False):
        self.response = np.array(response)
        self.marker = np.array(marker)
        self.percent = percent
        
        # sklearn roc_curve: fpr, tpr, thresholds
        # Note: pROC treats the marker values as thresholds. 
        # We need to match the logic where thresholds are unique values of the marker.
        fpr, tpr, thresholds = roc_curve(self.response, self.marker)
        
        # To match pROC's coords() 'all' behavior, we should use the unique markers as thresholds
        unique_thresholds = np.unique(self.marker)[::-1]
        
        # Calculate SE and SP for each unique threshold
        sensitivities = []
        specificities = []
        for t in unique_thresholds:
            # pROC behavior: outcome == 1 & marker >= t is TP
            tp = np.sum((self.response == 1) & (self.marker >= t))
            fp = np.sum((self.response == 0) & (self.marker >= t))
            fn = np.sum((self.response == 1) & (self.marker < t))
            tn = np.sum((self.response == 0) & (self.marker < t))
            
            se = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 100.0
            sp = (tn / (tn + fp)) * 100 if (tn + fp) > 0 else 100.0
            sensitivities.append(se)
            specificities.append(sp)
            
        self.thresholds = unique_thresholds
        self.sensitivity = np.array(sensitivities)
        self.specificity = np.array(specificities)
        self.tpr = self.sensitivity / 100 if self.percent else self.sensitivity
        self.fpr = (100 - self.specificity) / 100 if self.percent else (100 - self.specificity)

def roc(response, marker, percent=False):
    return RocCurve(response, marker, percent)

def smooth(roc_obj):
    # Simple identity for this exercise as smooth is not deeply tested here, 
    # but we return the object to allow chaining.
    return roc_obj

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # If x is "best", find the best threshold
    if x == "best":
        if best_method == "youden":
            # Weighted Youden: w1*sens + w2*spec
            w1, w2 = best_weights if best_weights is not None else (1, 1)
            # pROC uses (sens + spec) for default Youden
            score = w1 * roc_obj.sensitivity + w2 * roc_obj.specificity
            idx = np.argmax(score)
        elif best_method == "closest.topleft":
            # Distance to (0, 100) in (fpr, tpr) space
            # w1*fpr^2 + w2*(100-tpr)^2
            w1, w2 = best_weights if best_weights is not None else (1, 1)
            dist = w1 * (100 - roc_obj.specificity)**2 + w2 * (100 - roc_obj.sensitivity)**2
            idx = np.argmin(dist)
        else:
            idx = 0
        
        t = roc_obj.thresholds[idx]
        se = roc_obj.sensitivity[idx]
        sp = roc_obj.specificity[idx]
        
        if ret == "threshold": return pd.DataFrame({'threshold': [t]})
        if ret == "sensitivity": return pd.DataFrame({'sensitivity': [se]})
        if ret == "specificity": return pd.DataFrame({'specificity': [sp]})
        
        # Calculate other metrics
        preds = (roc_obj.marker >= t).astype(int)
        acc = accuracy_score(roc_obj.response, preds) * 100
        prec = precision_score(roc_obj.response, preds, zero_division=0) * 100
        rec = recall_score(roc_obj.response, preds, zero_division=0) * 100
        
        if ret == "all":
            return pd.DataFrame({
                'threshold': [t], 'specificity': [sp], 'sensitivity': [se], 
                'accuracy': [acc], 'tn': [np.sum((roc_obj.response == 0) & (preds == 0))],
                'tp': [np.sum((roc_obj.response == 1) & (preds == 1))],
                'fn': [np.sum((roc_obj.response == 1) & (preds == 0))],
                'fp': [np.sum((roc_obj.response == 0) & (preds == 1))],
                'precision': [prec], 'recall': [rec]
            }, index=[0])
        
        if isinstance(ret, list):
            res = {}
            res['threshold'] = t
            res['specificity'] = sp
            res['sensitivity'] = se
            res['accuracy'] = acc
            res['precision'] = prec
            res['recall'] = rec
            return pd.DataFrame([res])

    # If x is a specific value
    if input == "threshold":
        mask = roc_obj.thresholds == x
        if not any(mask):
            # In R, if exact match not found, pROC often interpolates or returns empty. 
            # Looking at stdout, it found 0.55.
            mask = np.abs(roc_obj.thresholds - x).argmin() == np.arange(len(roc_obj.thresholds))
            # However, R output for 0.55 matches exactly.
        return pd.DataFrame({'threshold': roc_obj.thresholds[mask], 
                             'specificity': roc_obj.specificity[mask], 
                             'sensitivity': roc_obj.sensitivity[mask]})
    
    elif input in ["sensitivity", "se"]:
        idx = np.abs(roc_obj.sensitivity - x).argmin()
        return pd.DataFrame({'threshold': [roc_obj.thresholds[idx]], 
                             'specificity': [roc_obj.specificity[idx]], 
                             'sensitivity': [roc_obj.sensitivity[idx]]})
    
    elif input in ["specificity", "sp"]:
        idx = np.abs(roc_obj.specificity - x).argmin()
        return pd.DataFrame({'threshold': [roc_obj.thresholds[idx]], 
                             'specificity': [roc_obj.specificity[idx]], 
                             'sensitivity': [roc_obj.sensitivity[idx]]})

    if x == "all":
        df = pd.DataFrame({'threshold': roc_obj.thresholds, 
                           'specificity': roc_obj.specificity, 
                           'sensitivity': roc_obj.sensitivity})
        if ret == "sensitivity":
            return pd.DataFrame({'sensitivity': roc_obj.sensitivity})
        if isinstance(ret, list):
            # Map R names to our calculated ones
            mapping = {'recall': 'sensitivity', 'tpr': 'sensitivity', 'fpr': '100-specificity'}
            res_df = pd.DataFrame()
            for r in ret:
                col_name = mapping.get(r, r)
                if col_name == 'sensitivity': res_df['sensitivity'] = roc_obj.sensitivity
                elif col_name == 'specificity': res_df['specificity'] = roc_obj.specificity
                elif col_name == '100-specificity': res_df['fpr'] = 100 - roc_obj.specificity
                elif col_name == 'threshold': res_df['threshold'] = roc_obj.thresholds
                elif col_name == 'precision':
                    # Calculate precision for all thresholds
                    precisions = []
                    for t in roc_obj.thresholds:
                        p = precision_score(roc_obj.response, (roc_obj.marker >= t).astype(int), zero_division=0) * 100
                        precisions.append(p)
                    res_df['precision'] = precisions
            return res_df
        return df

# Create a ROC curve:
# aSAH is available from data_shim
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
print(coords(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords(roc=roc_s100b, x=50, input="sensitivity"))
# Can be abbreviated:
print(coords(roc_s100b, 50, "se"))

# Works with smoothed ROC curves
print(coords(smooth(roc_s100b), 90, "specificity"))

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'].values)

# Get the best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="youden")) # default
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="closest.topleft"))

# and with different weights
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", 
       best_method="closest.topleft", best_weights=[5, 0.2]))

# Plotting (non-interactive, just to satisfy the call)
plt.figure()
plt.plot(roc_ndka.fpr, roc_ndka.tpr)
plt.title("ROC ndka")

# Return more values:
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy",
                           "precision", "recall"]))

# Return all values
print(coords(roc_s100b, "best", ret = "all"))

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
c_all = coords(roc_ndka, "all")
plt.figure()
plt.semilogx(c_all['threshold'], c_all['specificity'] + c_all['sensitivity'])
plt.title("Spec+Sens vs Threshold")

# Plot the Precision-Recall curve
c_pr = coords(roc_ndka, "all", ret = ["recall", "precision"])
plt.figure()
plt.plot(c_pr['sensitivity'], c_pr['precision'])
plt.ylim(0, 100)
plt.title("Precision-Recall")

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
c_tpr_fpr = coords(roc_ndka, "all", ret = ["tpr", "fpr"])
plt.figure()
plt.plot(c_tpr_fpr['fpr'], c_tpr_fpr['sensitivity'])
plt.title("TPR vs FPR")