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

class ROC:
    def __init__(self, response, predictor, percent=True):
        self.response = np.array(response)
        self.predictor = np.array(predictor)
        self.percent = percent
        
        # sklearn.metrics.roc_curve returns fpr, tpr, thresholds
        # thresholds[0] is always a value that makes all predictions negative
        fpr, tpr, thresholds = roc_curve(self.response, self.predictor)
        
        # pROC by default sorts thresholds descending
        # sklearn returns them sorted descending except for the first element
        self.fpr = fpr
        self.tpr = tpr
        self.thresholds = thresholds
        
    def smooth(self):
        # Simplified smoothing approximation for coords purpose
        return self

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # Extract basic metrics
    tpr = roc_obj.tpr
    fpr = roc_obj.fpr
    thresh = roc_obj.thresholds
    
    # Scale to percent if requested
    se = tpr * 100 if roc_obj.percent else tpr
    sp = (1 - fpr) * 100 if roc_obj.percent else (1 - fpr)
    
    if x == "best":
        if best_method == "youden":
            # Youden J = Sensitivity + Specificity - 100 (if percent)
            weights = best_weights if best_weights is not None else [1, 1]
            score = weights[0] * se + weights[1] * sp
            idx = np.argmax(score)
        elif best_method == "closest.topleft":
            # Closest to (0, 100) in ROC space
            weights = best_weights if best_weights is not None else [1, 1]
            # distance = sqrt( w1*fpr^2 + w2*(1-tpr)^2 )
            dist = np.sqrt(weights[0] * (fpr**2) + weights[1] * ((1-tpr)**2))
            idx = np.argmin(dist)
        else:
            idx = 0
    elif input == "sensitivity" or (isinstance(x, (int, float)) and input == "se"):
        # Find threshold closest to target sensitivity
        target = x if input == "sensitivity" else x
        idx = np.argmin(np.abs(se - target))
    elif input == "specificity":
        target = x
        idx = np.argmin(np.abs(sp - target))
    elif isinstance(x, (int, float)):
        # x is a threshold
        # Find index where threshold is closest to x
        idx = np.argmin(np.abs(thresh - x))
    elif x == "all":
        # return dataframe of all thresholds
        df = pd.DataFrame({
            'threshold': thresh,
            'specificity': sp,
            'sensitivity': se
        })
        # Add standard ROC metrics
        df['tpr'] = tpr
        df['fpr'] = fpr
        # Precision/Recall needs raw data
        # This is an approximation for the 'all' case
        return df
    else:
        idx = 0

    # Calculate point-specific metrics
    t_val = thresh[idx]
    pred = (roc_obj.predictor >= t_val).astype(int)
    
    # Sensitivity and Specificity
    res = {
        'threshold': t_val,
        'specificity': sp[idx],
        'sensitivity': se[idx],
    }
    
    if ret == "all" or any(m in ret for m in ["accuracy", "precision", "recall", "tpr", "fpr"]):
        res['accuracy'] = accuracy_score(roc_obj.response, pred) * 100
        res['precision'] = precision_score(roc_obj.response, pred, zero_division=0) * 100
        res['recall'] = recall_score(roc_obj.response, pred, zero_division=0) * 100
        res['tpr'] = tpr[idx] * 100
        res['fpr'] = fpr[idx] * 100
        # Add pROC specific metrics
        res['tn'] = np.sum((pred == 0) & (roc_obj.response == 0))
        res['tp'] = np.sum((pred == 1) & (roc_obj.response == 1))
        res['fn'] = np.sum((pred == 0) & (roc_obj.response == 1))
        res['fp'] = np.sum((pred == 1) & (roc_obj.response == 0))
        res['npv'] = (res['tn'] / (res['tn'] + res['fn'])) * 100 if (res['tn'] + res['fn']) != 0 else 0
        res['ppv'] = (res['tp'] / (res['tp'] + res['fp'])) * 100 if (res['tp'] + res['fp']) != 0 else 0
        res['fdr'] = (res['fp'] / (res['tp'] + res['fp'])) * 100 if (res['tp'] + res['fp']) != 0 else 0
        res['tnr'] = res['specificity']
        res['fnr'] = 100 - res['sensitivity']
        res['lr_pos'] = (res['sensitivity']/100) / (1 - res['specificity']/100) if res['specificity'] != 100 else np.inf
        res['lr_neg'] = (1 - res['sensitivity']/100) / (res['specificity']/100) if res['specificity'] != 0 else np.inf
        res['youden'] = res['sensitivity'] + res['specificity'] - 100
        res['closest.topleft'] = np.sqrt(fpr[idx]**2 + (1-tpr[idx])**2)

    if ret == "threshold":
        return pd.DataFrame({'threshold': [res['threshold']]})
    elif ret == "sensitivity":
        return pd.DataFrame({'sensitivity': [res['sensitivity']]})
    elif isinstance(ret, list):
        return pd.DataFrame([ {k: res[k] for k in ret} ])
    elif ret == "all":
        return pd.Series(res)
    else:
        # Default return (similar to coords(roc, 0.55))
        return pd.DataFrame({'threshold': [res['threshold']], 'specificity': [res['specificity']], 'sensitivity': [res['sensitivity']]})

# Main script
roc_s100b = ROC(aSAH['outcome'], aSAH['s100b'], percent=True)
print(coords(roc_s100b, 0.55))

print(coords(roc=roc_s100b, x=50, input="sensitivity"))
print(coords(roc_s100b, 50, "se"))

print(coords(roc_s100b.smooth(), 90, "specificity"))

cc = coords(roc_s100b, "all", ret="sensitivity")
# If 'all' was returned as a DF
if isinstance(cc, pd.DataFrame):
    print(cc['sensitivity'])
else:
    print(cc)

print(coords(roc_s100b, "best", ret="threshold"))

roc_ndka = ROC(aSAH['outcome'], aSAH['ndka'], percent=True)
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# plot(roc.ndka, ...) - simulate plot by printing summary
best_idx_ndka = np.argmax(roc_ndka.tpr + (1 - roc_ndka.fpr)) # Youden
print(f"Plotting ROC with best threshold: {roc_ndka.thresholds[best_idx_ndka]}")

print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))
print(coords(roc_s100b, "best", ret="all"))

# Sensitivity + Specificity vs Threshold
df_all_ndka = coords(roc_ndka, "all")
plt.figure()
plt.plot(df_all_ndka['threshold'], df_all_ndka['specificity'] + df_all_ndka['sensitivity'])
plt.xscale('log')
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# Precision-Recall curve
prec, rec, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec * 100, prec * 100)
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# TPR vs FPR
plt.figure()
plt.plot(roc_ndka.fpr * 100, roc_ndka.tpr * 100)
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()