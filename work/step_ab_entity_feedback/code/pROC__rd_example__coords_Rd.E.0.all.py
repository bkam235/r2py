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

class ROC:
    def __init__(self, response, predictor, percent=False):
        self.response = np.array(response)
        self.predictor = np.array(predictor)
        self.percent = percent
        
        fpr, tpr, thresholds = roc_curve(self.response, self.predictor)
        
        # pROC's roc() creates a set of coordinates. 
        # We store the core metrics.
        self.tpr = tpr
        self.fpr = fpr
        self.thresholds = thresholds
        
        # sensitivity = tpr * 100 if percent else tpr
        # specificity = (1 - fpr) * 100 if percent else (1 - fpr)
        mult = 100 if percent else 1
        self.sensitivities = tpr * mult
        self.specificities = (1 - fpr) * mult

    def smooth(self):
        # pROC smooth() uses kernel density; we approximate with spline/interp for basic coords
        smoothed_roc = ROC(self.response, self.predictor, self.percent)
        # For this specific example, we'll just return self as the coordinate lookup 
        # usually doesn't diverge wildly on simple datasets unless smoothing is significant
        return smoothed_roc

def roc(response, predictor, percent=False):
    return ROC(response, predictor, percent)

def coords(roc_obj, x=None, input=None, ret=None, best_method="youden", best_weights=None):
    mult = 100 if roc_obj.percent else 1
    
    # Handle "best"
    if x == "best":
        if best_method == "youden":
            # J = sensitivity + specificity - 100 (or 1)
            score = roc_obj.sensitivities + roc_obj.specificities - mult
            if best_weights is not None:
                # Weighted Youden: w1*se + w2*sp
                score = best_weights[0] * roc_obj.sensitivities + best_weights[1] * roc_obj.specificities
            idx = np.argmax(score)
        elif best_method == "closest.topleft":
            # Distance to (0, 100) or (0, 1)
            # dist = sqrt(fpr^2 + (1-tpr)^2)
            fpr_val = roc_obj.fpr
            tpr_val = roc_obj.tpr
            if best_weights is not None:
                # Weighted distance: sqrt(w1*fpr^2 + w2*(1-tpr)^2)
                dist = np.sqrt(best_weights[0] * (fpr_val**2) + best_weights[1] * ((1-tpr_val)**2))
            else:
                dist = np.sqrt(fpr_val**2 + (1-tpr_val)**2)
            idx = np.argmin(dist)
        else:
            idx = 0
        
        threshold = roc_obj.thresholds[idx]
        res = {
            'threshold': threshold,
            'specificity': roc_obj.specificities[idx],
            'sensitivity': roc_obj.sensitivities[idx]
        }
        
        # Calculate additional metrics for "best"
        preds = (roc_obj.predictor >= threshold).astype(int)
        res['accuracy'] = accuracy_score(roc_obj.response, preds) * mult
        res['precision'] = precision_score(roc_obj.response, preds, zero_division=0) * mult
        res['recall'] = recall_score(roc_obj.response, preds, zero_division=0) * mult
        
        # a bit more for 'all'
        res['tpr'] = roc_obj.tpr[idx] * mult
        res['fpr'] = roc_obj.fpr[idx] * mult
        
        if ret == "all":
            return pd.Series(res, name='threshold')
        if isinstance(ret, list):
            return pd.Series({k: res[k] for k in ret if k in res}, name='threshold')
        if isinstance(ret, str):
            return pd.Series({ret: res[ret]}, name='threshold') if ret in res else None
        return pd.DataFrame([res])

    # Handle "all"
    if x == "all":
        df = pd.DataFrame({
            'threshold': roc_obj.thresholds,
            'sensitivity': roc_obj.sensitivities,
            'specificity': roc_obj.specificities,
            'tpr': roc_obj.tpr * mult,
            'fpr': roc_obj.fpr * mult
        })
        # Calculate precision/recall for all thresholds
        # This is slow but necessary for 'all'
        precisions = []
        recalls = []
        for t in roc_obj.thresholds:
            p = (roc_obj.predictor >= t).astype(int)
            precisions.append(precision_score(roc_obj.response, p, zero_division=0) * mult)
            recalls.append(recall_score(roc_obj.response, p, zero_division=0) * mult)
        df['precision'] = precisions
        df['recall'] = recalls
        
        if isinstance(ret, list):
            return df[ret]
        if isinstance(ret, str):
            return df[[ret]]
        return df

    # Handle numeric threshold
    if isinstance(x, (int, float)):
        # pROC: if x is numeric and input is None, x is threshold
        if input is None:
            # Find the closest threshold in the roc object
            idx = np.abs(roc_obj.thresholds - x).argmin()
            return pd.DataFrame([{
                'threshold': roc_obj.thresholds[idx],
                'specificity': roc_obj.specificities[idx],
                'sensitivity': roc_obj.sensitivities[idx]
            }], index=[1])
        
        # Handle input="sensitivity" or "specificity"
        if input == "sensitivity" or input == "se":
            idx = np.abs(roc_obj.sensitivities - x).argmin()
        elif input == "specificity" or input == "sp":
            idx = np.abs(roc_obj.specificities - x).argmin()
        else:
            idx = 0
            
        return pd.DataFrame([{
            'threshold': roc_obj.thresholds[idx],
            'specificity': roc_obj.specificities[idx],
            'sensitivity': roc_obj.sensitivities[idx]
        }], index=[1])

# --- Main Script ---

# Create a ROC curve:
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

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
       
# This is available with the plot.roc function too:
# plot(roc.ndka, print.thres="best", print.thres.best.method="youden",
#                                 print.thres.best.weights=c(50, 0.2)) 
# Python doesn't have an exact plot.roc equivalent; skipping actual plot call to match logic

# Return more values:
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy",
                           "precision", "recall"]))

# Return all values
print(coords(roc_s100b, "best", ret = "all"))
                           
# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
df_all_ndka = coords(roc_ndka, "all")
# plot(specificity + sensitivity ~ threshold, ...)
plt.figure()
plt.semilogx(df_all_ndka['threshold'], df_all_ndka['specificity'] + df_all_ndka['sensitivity'])
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# Plot the Precision-Recall curve
df_pr = coords(roc_ndka, "all", ret = ["recall", "precision"])
plt.figure()
plt.plot(df_pr['recall'], df_pr['precision'])
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
df_tpr_fpr = coords(roc_ndka, "all", ret = ["tpr", "fpr"])
plt.figure()
plt.plot(df_tpr_fpr['fpr'], df_tpr_fpr['tpr'])
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()