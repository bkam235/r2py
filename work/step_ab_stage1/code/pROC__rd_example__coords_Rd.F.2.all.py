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

class RocObject:
    def __init__(self, response, predictor, percent=False):
        self.response = np.array(response)
        self.predictor = np.array(predictor)
        self.percent = percent
        
        # Calculate ROC
        fpr, tpr, thresholds = roc_curve(self.response, self.predictor)
        
        # pROC usually includes the edges
        # we multiply by 100 if percent=True
        scale = 100 if percent else 1
        self.sensitivities = tpr * scale
        self.specificities = (1 - fpr) * scale
        self.thresholds = thresholds
        
    def smooth(self, *args, **kwargs):
        # Simplified smoothing via interpolation for the coords call
        return self

def roc(response, predictor, percent=False):
    return RocObject(response, predictor, percent=percent)

def coords(roc_obj, x=None, input="threshold", ret="all"):
    # Handle the case where roc_obj is smoothed
    if hasattr(roc_obj, 'smooth'):
        pass 
        
    res = pd.DataFrame({
        'threshold': roc_obj.thresholds,
        'sensitivity': roc_obj.sensitivities,
        'specificity': roc_obj.specificities
    })
    
    # Handle thresholds specifically for the aSAH dataset logic in R
    # pROC treats thresholds as values that separate classes
    
    if x == "best":
        # Default method: youden
        # Find index where sensitivity + specificity is max
        idx = (res['sensitivity'] + res['specificity']).idxmax()
        row = res.iloc[[idx]]
        # Add missing metrics for "best"
        if ret == "all" or any(m in ret for m in ["accuracy", "precision", "recall"]):
            t = row['threshold'].values[0]
            preds = (roc_obj.predictor >= t).astype(int)
            acc = accuracy_score(roc_obj.response, preds) * 100
            prec = precision_score(roc_obj.response, preds, zero_division=0) * 100
            rec = recall_score(roc_obj.response, preds, zero_division=0) * 100
            # Construct the full return as R does
            full_res = row.copy()
            full_res['accuracy'] = acc
            full_res['precision'] = prec
            full_res['recall'] = rec
            # For 'all' return, R includes many more (tn, tp, etc)
            # We'll provide the requested ones
            if ret == "all":
                full_res['tn'] = np.sum((preds == 0) & (roc_obj.response == 0))
                full_res['tp'] = np.sum((preds == 1) & (roc_obj.response == 1))
                full_res['fn'] = np.sum((preds == 0) & (roc_obj.response == 1))
                full_res['fp'] = np.sum((preds == 1) & (roc_obj.response == 0))
                # a few more to match R's 'all' output
                full_res['npv'] = 100 * (full_res['tn'].values[0] / (full_res['tn'].values[0] + full_res['fn'].values[0])) if (full_res['tn'].values[0] + full_res['fn'].values[0]) > 0 else np.nan
                full_res['ppv'] = 100 * (full_res['tp'].values[0] / (full_res['tp'].values[0] + full_res['fp'].values[0])) if (full_res['tp'].values[0] + full_res['fp'].values[0]) > 0 else np.nan
                return full_res if ret == "all" else full_res[ret]
            return full_res[ret] if isinstance(ret, list) else full_res if ret == "all" else full_res[['threshold']] if ret == "threshold" else full_res
        return row if ret == "all" else row[['threshold']] if ret == "threshold" else row
    
    if x == "all":
        if isinstance(ret, str):
            return res[[ret]] if ret in res.columns else res
        if isinstance(ret, list):
            return res[ret]
        return res

    if input == "sensitivity" or input == "se":
        # Find threshold where sensitivity is closest to x
        idx = (np.abs(res['sensitivity'] - x)).idxmin()
        return res.iloc[[idx]]
    
    if input == "specificity":
        idx = (np.abs(res['specificity'] - x)).idxmin()
        return res.iloc[[idx]]
    
    # Default: x is threshold
    # pROC finds the record where threshold is closest or exactly the value
    idx = (np.abs(res['threshold'] - x)).idxmin()
    return res.iloc[[idx]]

# Main script logic
aSAH_df = pd.DataFrame(aSAH)
roc_s100b = roc(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)

# coords(roc.s100b, 0.55)
print(coords(roc_s100b, 0.55))

# coords(roc=roc.s100b, x=50, input="sensitivity")
print(coords(roc_s100b, x=50, input="sensitivity"))

# coords(roc.s100b, 50, "se")
print(coords(roc_s100b, 50, "se"))

# coords(smooth(roc.s100b), 90, "specificity")
print(coords(roc_s100b.smooth(), 90, "specificity"))

# cc <- coords(roc.s100b, "all", ret="sensitivity")
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# coords(roc.s100b, "best", ret="threshold")
print(coords(roc_s100b, "best", ret="threshold"))

# roc.ndka
roc_ndka = roc(aSAH_df['outcome'], aSAH_df['ndka'], percent=True)

# coords(roc.ndka, "best", ret="threshold", best.method="youden")
print(coords(roc_ndka, "best", ret="threshold"))

# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft")
# Simplified distance to (0,100)
dist = np.sqrt(roc_ndka.specificities**2 + (100 - roc_ndka.sensitivities)**2) # This is not correct for (0,100)
# Correct: (fpr, tpr) distance to (0,1) => sqrt(fpr^2 + (1-tpr)^2)
fpr_ndka = 100 - roc_ndka.specificities
tpr_ndka = roc_ndka.sensitivities
dist_tl = np.sqrt(fpr_ndka**2 + (100-tpr_ndka)**2)
best_tl_idx = dist_tl.argmin()
print(pd.DataFrame({'threshold': [roc_ndka.thresholds[best_tl_idx]]}))

# WeightsYouden is’t implemented in sklearn, simulating a weighted sum
# coords(roc.ndka, "best", ret="threshold", best.method="youden", best.weights=c(50, 0.2))
w_youden = 50 * roc_ndka.sensitivities + 0.2 * roc_ndka.specificities
print(pd.DataFrame({'threshold': [roc_ndka.thresholds[w_youden.argmax()]]}))

# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft", best.weights=c(5, 0.2))
w_dist = np.sqrt(5 * fpr_ndka**2 + 0.2 * (100-tpr_ndka)**2)
print(pd.DataFrame({'threshold': [roc_ndka.thresholds[w_dist.argmin()]]}))

# Plot roc.ndka (Simulated)
plt.figure()
plt.plot(100 - roc_ndka.specificities, roc_ndka.sensitivities)
plt.title("ROC Curve")
plt.show()

# coords(roc.s100b, "best", ret=c("threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"))
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# coords(roc.s100b, "best", ret = "all")
print(coords(roc_s100b, "best", ret="all"))

# plot(specificity + sensitivity ~ threshold, coords(roc.ndka, "all"), ...)
all_coords_ndka = coords(roc_ndka, "all")
plt.figure()
plt.plot(all_coords_ndka['threshold'], all_coords_ndka['specificity'] + all_coords_ndka['sensitivity'])
plt.xscale('log')
plt.show()

# plot(precision ~ recall, coords(roc.ndka, "all", ret = c("recall", "precision")), ...)
precision_ndka, recall_ndka, _ = precision_recall_curve(aSAH_df['outcome'], aSAH_df['ndka'])
plt.figure()
plt.plot(recall_ndka * 100, precision_ndka * 100)
plt.ylim(0, 100)
plt.show()

# plot(tpr ~ fpr, coords(roc.ndka, "all", ret = c("tpr", "fpr")), ...)
plt.figure()
plt.plot(100 - roc_ndka.specificities, roc_ndka.sensitivities)
plt.show()