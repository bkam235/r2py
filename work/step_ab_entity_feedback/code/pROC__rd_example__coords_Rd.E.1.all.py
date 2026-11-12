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

class ROCCurve:
    def __init__(self, response, marker, percent=True):
        self.response = np.array(response)
        self.marker = np.array(marker)
        self.percent = percent
        fpr, tpr, thresholds = roc_curve(self.response, self.marker)
        
        # pROC usually includes thresholds that result in 0 and 100% sensitivity
        # sklearn's thresholds may be shorter than fpr/tpr
        self.fpr = fpr
        self.tpr = tpr
        # In pROC, thresholds are the values used for cut-offs
        # we extend thresholds to match fpr/tpr length by adding a max value
        self.thresholds = np.concatenate(([thresholds[0]] * (len(fpr) - len(thresholds)), thresholds))
        
    def get_coords(self, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
        # Create the base dataframe
        df = pd.DataFrame({
            'threshold': self.thresholds,
            'sensitivity': self.tpr * (100 if self.percent else 1),
            'specificity': (1 - self.fpr) * (100 if self.percent else 1),
            'tpr': self.tpr,
            'fpr': self.fpr
        })
        
        if x == "best":
            if best_method == "youden":
                if best_weights is None:
                    # Youden: sens + spec - 1 (or 100)
                    score = df['sensitivity'] + df['specificity'] - (100 if self.percent else 1)
                else:
                    score = best_weights[0] * df['sensitivity'] + best_weights[1] * df['specificity']
                idx = score.idxmax()
            elif best_method == "closest.topleft":
                if best_weights is None:
                    # Dist to (0, 1) in ROC space
                    dist = np.sqrt(df['fpr']**2 + (1 - df['tpr'])**2)
                else:
                    dist = np.sqrt(best_weights[0] * df['fpr']**2 + best_weights[1] * (1 - df['tpr'])**2)
                idx = dist.idxmin()
            
            row = df.iloc[[idx]].copy()
            # Calculate additional metrics for "best"
            thresh = row['threshold'].values[0]
            preds = (self.marker >= thresh).astype(int)
            row['accuracy'] = accuracy_score(self.response, preds) * 100
            row['precision'] = precision_score(self.response, preds, zero_division=0) * 100
            row['recall'] = recall_score(self.response, preds, zero_division=0) * 100
            row['tn'] = ((preds == 0) & (self.response == 0)).sum()
            row['tp'] = ((preds == 1) & (self.response == 1)).sum()
            row['fn'] = ((preds == 0) & (self.response == 1)).sum()
            row['fp'] = ((preds == 1) & (self.response == 0)).sum()
            row['npv'] = (row['tn'].values[0] / (row['tn'].values[0] + row['fn'].values[0]) * 100) if (row['tn'].values[0] + row['fn'].values[0]) > 0 else 0
            row['ppv'] = (row['tp'].values[0] / (row['tp'].values[0] + row['fp'].values[0]) * 100) if (row['tp'].values[0] + row['fp'].values[0]) > 0 else 0
            row['fdr'] = 100 - row['ppv'].values[0]
            row['fpr'] = row['fpr'].values[0]
            row['tpr'] = row['tpr'].values[0]
            row['tnr'] = row['specificity'].values[0]
            row['fnr'] = 100 - row['sensitivity'].values[0]
            row['1-specificity'] = 100 - row['specificity'].values[0]
            row['1-sensitivity'] = 100 - row['sensitivity'].values[0]
            row['1-accuracy'] = 100 - row['accuracy'].values[0]
            row['1-npv'] = 100 - row['npv'].values[0]
            row['1-ppv'] = 100 - row['ppv'].values[0]
            row['precision'] = row['precision'].values[0]
            row['recall'] = row['recall'].values[0]
            row['lr_pos'] = (row['sensitivity'].values[0] / row['fpr'].values[0]) if row['fpr'].values[0] != 0 else np.inf
            row['lr_neg'] = (row['specificity'].values[0] / (100 - row['sensitivity'].values[0])) if (100 - row['sensitivity'].values[0]) != 0 else np.inf
            row['youden'] = row['sensitivity'].values[0] + row['specificity'].values[0] - 100
            row['closest.topleft'] = np.sqrt(row['fpr'].values[0]**2 + (1-row['tpr'].values[0])**2) * 100
            
            if ret == "all":
                return row
            elif isinstance(ret, list):
                return row[ret]
            else:
                return row[[ret]]
        
        elif x == "all":
            if ret == "all":
                return df
            elif isinstance(ret, list):
                return df[ret]
            else:
                return df[[ret]]
        
        else:
            # Numeric x is treated as threshold
            if input == "threshold":
                idx = (np.abs(df['threshold'] - x)).idxmin()
                row = df.iloc[[idx]]
            elif input == "sensitivity" or input == "se":
                idx = (np.abs(df['sensitivity'] - x)).idxmin()
                row = df.iloc[[idx]]
            elif input == "specificity" or input == "sp":
                idx = (np.abs(df['specificity'] - x)).idxmin()
                row = df.iloc[[idx]]
            else:
                row = df.iloc[[0]]
            
            if ret == "all":
                return row
            elif isinstance(ret, list):
                return row[ret]
            else:
                return row[[ret]]

def roc(response, marker, percent=True):
    return ROCCurve(response, marker, percent=percent)

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    return roc_obj.get_coords(x=x, input=input, ret=ret, best_method=best_method, best_weights=best_weights)

def smooth(roc_obj):
    # Simplified smoothing for simulation: just return the original object as smooth is complex
    return roc_obj

# Execution
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)
print(coords(roc_s100b, 0.55))

print(coords(roc=roc_s100b, x=50, input="sensitivity"))
print(coords(roc_s100b, 50, "se"))

print(coords(smooth(roc_s100b), 90, "specificity"))

cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'].values)

print(coords(roc_s100b, "best", ret="threshold"))

roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# Simulation of plot.roc
plt.figure()
plt.plot(roc_ndka.fpr, roc_ndka.tpr)
plt.title("ROC Curve")
plt.xlabel("FPR")
plt.ylabel("TPR")
# print.thres logic skipped as it's purely visual in R plot.roc

print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))
print(coords(roc_s100b, "best", ret="all"))

# plot(specificity + sensitivity ~ threshold, coords(roc.ndka, "all"), type = "l", log="x", subset = is.finite(threshold))
all_coords_ndka = coords(roc_ndka, "all")
plt.figure()
plt.semilogx(all_coords_ndka['threshold'], all_coords_ndka['specificity'] + all_coords_ndka['sensitivity'])
plt.title("Spec+Sens vs Threshold")
plt.show()

# plot(precision ~ recall, coords(roc.ndka, "all", ret = c("recall", "precision")), type="l", ylim = c(0, 100))
prec, rec, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec * 100, prec * 100)
plt.ylim(0, 100)
plt.title("Precision-Recall Curve")
plt.show()

# plot(tpr ~ fpr, coords(roc.ndka, "all", ret = c("tpr", "fpr")), type="l")
plt.figure()
plt.plot(roc_ndka.fpr, roc_ndka.tpr)
plt.title("TPR vs FPR")
plt.show()