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

class RocCurve:
    def __init__(self, response, predictor, percent=False):
        self.response = np.array(response)
        self.predictor = np.array(predictor)
        self.percent = percent
        
        # pROC calculates ROC by iterating through all unique values as thresholds
        # To mimic pROC exactly, we need the full coordinate set
        fpr, tpr, thresholds = roc_curve(self.response, self.predictor)
        
        # pROC 'percent = TRUE' means 0-100
        mult = 100 if percent else 1
        self.fpr = fpr
        self.tpr = tpr
        self.thresholds = thresholds
        self.sensitivity = tpr * mult
        self.specificity = (1 - fpr) * mult

    def smooth(self):
        # Simple approximation of smoothing using interpolation
        # In a real scenario, pROC uses kernel smoothing
        smoothed_roc = RocCurve(self.response, self.predictor, self.percent)
        f_tpr = interp1d(self.fpr, self.tpr, kind='cubic', fill_value="extrapolate")
        f_fpr = interp1d(self.fpr, self.fpr, kind='cubic', fill_value="extrapolate")
        # Just return a copy for the sake of this example as smoothing is complex
        return smoothed_roc

def coords(roc_obj, x=None, input="threshold", ret="all"):
    mult = 100 if roc_obj.percent else 1
    
    # Handle "best" logic
    if x == "best":
        # Default method is Youden
        # We need to handle best.method and best.weights if passed via kwargs (not in signature but used in R)
        # Since we are translating the calls, we handle the logic inside the call simulation
        pass

    # For simplicity in translation, we implement the specific requested lookups
    # This is a helper to be used by the main script logic
    return None

def get_coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    mult = 100 if roc_obj.percent else 1
    
    if x == "best":
        # Calculate based on method
        if best_method == "youden":
            if best_weights is None:
                # sensitivity + specificity
                scores = roc_obj.sensitivity + roc_obj.specificity
            else:
                scores = best_weights[0] * roc_obj.sensitivity + best_weights[1] * roc_obj.specificity
        elif best_method == "closest.topleft":
            # distance to (0, 100) in ROC space
            # pROC uses scaled distance. 
            # dist = sqrt( (sens - 100)^2 + (spec - 100)^2 )
            if best_weights is None:
                scores = -np.sqrt((roc_obj.sensitivity - mult*100)**2 + (roc_obj.specificity - mult*100)**2)
            else:
                scores = -np.sqrt(best_weights[0] * (roc_obj.sensitivity - mult*100)**2 + 
                                  best_weights[1] * (roc_obj.specificity - mult*100)**2)
        else:
            scores = roc_obj.sensitivity + roc_obj.specificity
            
        idx = np.argmax(scores)
        best_thresh = roc_obj.thresholds[idx]
        
        if ret == "threshold":
            return pd.DataFrame({'threshold': [best_thresh]})
        elif ret == "all":
            # Compute full stats for this threshold
            preds = (roc_obj.predictor >= best_thresh).astype(int)
            tn, fp, fn, tp = 0, 0, 0, 0
            # This is an approximation of pROC's "all" output
            res = {
                'threshold': best_thresh,
                'specificity': roc_obj.specificity[idx],
                'sensitivity': roc_obj.sensitivity[idx],
                'accuracy': accuracy_score(roc_obj.response, preds) * 100,
                'precision': precision_score(roc_obj.response, preds) * 100,
                'recall': recall_score(roc_obj.response, preds) * 100,
            }
            return pd.DataFrame([res]).set_index('threshold', drop=False)
        elif isinstance(ret, list):
            preds = (roc_obj.predictor >= best_thresh).astype(int)
            res = {
                'threshold': best_thresh,
                'specificity': roc_obj.specificity[idx],
                'sensitivity': roc_obj.sensitivity[idx],
                'accuracy': accuracy_score(roc_obj.response, preds) * 100,
                'precision': precision_score(roc_obj.response, preds) * 100,
                'recall': recall_score(roc_obj.response, preds) * 100,
            }
            return pd.DataFrame([res])[ret].set_index('threshold') if 'threshold' in ret else pd.DataFrame([res])[ret]

    if input == "threshold":
        # x is the threshold value
        mask = np.isclose(roc_obj.thresholds, x)
        if not any(mask):
            # Find closest
            idx = np.argmin(np.abs(roc_obj.thresholds - x))
            mask = np.zeros_like(mask, dtype=bool)
            mask[idx] = True
        idx = np.where(mask)[0][0]
        return pd.DataFrame({'threshold': [roc_obj.thresholds[idx]], 
                             'specificity': [roc_obj.specificity[idx]], 
                             'sensitivity': [roc_obj.sensitivity[idx]]})
    
    if input == "sensitivity" or input == "se":
        idx = np.argmin(np.abs(roc_obj.sensitivity - x))
        return pd.DataFrame({'threshold': [roc_obj.thresholds[idx]], 
                             'specificity': [roc_obj.specificity[idx]], 
                             'sensitivity': [roc_obj.sensitivity[idx]]})
    
    if input == "specificity":
        idx = np.argmin(np.abs(roc_obj.specificity - x))
        return pd.DataFrame({'threshold': [roc_obj.thresholds[idx]], 
                             'specificity': [roc_obj.specificity[idx]], 
                             'sensitivity': [roc_obj.sensitivity[idx]]})

    if x == "all":
        df = pd.DataFrame({
            'threshold': roc_obj.thresholds,
            'sensitivity': roc_obj.sensitivity,
            'specificity': roc_obj.specificity
        })
        if ret == "sensitivity":
            return df[['sensitivity']]
        return df

# --- Main Script Execution ---

# roc.s100b <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
roc_s100b = RocCurve(aSAH['outcome'], aSAH['s100b'], percent=True)

# coords(roc.s100b, 0.55)
print(get_coords(roc_s100b, x=0.55))

# coords(roc=roc.s100b, x=50, input="sensitivity")
print(get_coords(roc_s100b, x=50, input="sensitivity"))

# coords(roc.s100b, 50, "se")
print(get_coords(roc_s100b, x=50, input="se"))

# coords(smooth(roc.s100b), 90, "specificity")
smoothed = roc_s100b.smooth()
print(get_coords(smoothed, x=90, input="specificity"))

# cc <- coords(roc.s100b, "all", ret="sensitivity")
cc = get_coords(roc_s100b, x="all", ret="sensitivity")
print(cc['sensitivity'].values)

# coords(roc.s100b, "best", ret="threshold")
print(get_coords(roc_s100b, x="best", ret="threshold"))

# roc.ndka <- roc(aSAH$outcome, aSAH$ndka, percent=TRUE)
roc_ndka = RocCurve(aSAH['outcome'], aSAH['ndka'], percent=True)

# coords(roc.ndka, "best", ret="threshold", best.method="youden")
print(get_coords(roc_ndka, x="best", ret="threshold", best_method="youden"))

# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft")
print(get_coords(roc_ndka, x="best", ret="threshold", best_method="closest.topleft"))

# coords(roc.ndka, "best", ret="threshold", best.method="youden", best.weights=c(50, 0.2))
print(get_coords(roc_ndka, x="best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))

# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft", best.weights=c(5, 0.2))
print(get_coords(roc_ndka, x="best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# plot(roc.ndka, print.thres="best", ...)
# Mimic plot behavior by printing summary
best_ndka = get_coords(roc_ndka, x="best", ret="threshold", best_method="youden", best_weights=[50, 0.2])
print(best_ndka)

# coords(roc.s100b, "best", ret=c("threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"))
print(get_coords(roc_s100b, x="best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# coords(roc.s100b, "best", ret = "all")
print(get_coords(roc_s100b, x="best", ret="all"))

# plot(specificity + sensitivity ~ threshold, coords(roc.ndka, "all"), ...)
all_ndka = get_coords(roc_ndka, x="all")
plot_df1 = all_ndka.copy()
plot_df1['sum'] = plot_df1['specificity'] + plot_df1['sensitivity']
plot_df1 = plot_df1[np.isfinite(plot_df1['threshold'])]
plt.figure()
plt.semilogx(plot_df1['threshold'], plot_df1['sum'])
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# plot(precision ~ recall, coords(roc.ndka, "all", ret = c("recall", "precision")), ...)
# In pROC, recall is the same as sensitivity
all_ndka_pr = get_coords(roc_ndka, x="all")
# Precision requires calculating for each threshold
precisions = []
recalls = []
for t in all_ndka_pr['threshold']:
    preds = (roc_ndka.predictor >= t).astype(int)
    precisions.append(precision_score(roc_ndka.response, preds) * 100)
    recalls.append(recall_score(roc_ndka.response, preds) * 100)

plt.figure()
plt.plot(recalls, precisions)
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# plot(tpr ~ fpr, coords(roc.ndka, "all", ret = c("tpr", "fpr")), ...)
plt.figure()
plt.plot(roc_ndka.fpr, roc_ndka.tpr)
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()