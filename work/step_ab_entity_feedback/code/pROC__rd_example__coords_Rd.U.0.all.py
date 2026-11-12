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

class pROC_ROC:
    def __init__(self, response, marker, percent=False):
        self.response = np.array(response)
        self.marker = np.array(marker)
        self.percent = percent
        
        # pROC calculates thresholds based on unique values of the marker
        # It creates a curve by testing each unique value as a threshold
        self.thresholds = np.sort(np.unique(marker))[::-1]
        self.sensitivities = []
        self.specificities = []
        
        for t in self.thresholds:
            # pROC usually defines sensitivity as TPR where marker >= threshold
            preds = (self.marker >= t).astype(int)
            tp = np.sum((preds == 1) & (self.response == 1))
            fp = np.sum((preds == 1) & (self.response == 0))
            fn = np.sum((preds == 0) & (self.response == 1))
            tn = np.sum((preds == 0) & (self.response == 0))
            
            se = tp / (tp + fn) if (tp + fn) > 0 else 0
            sp = tn / (tn + fp) if (tn + fp) > 0 else 0
            self.sensitivities.append(se)
            self.specificities.append(sp)
        
        self.sensitivities = np.array(self.sensitivities)
        self.specificities = np.array(self.specificities)
        
        if self.percent:
            self.sensitivities *= 100
            self.specificities *= 100

    def coords(self, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
        # Scale constants
        scale = 100 if self.percent else 1
        
        if x == "best":
            if best_method == "youden":
                weights = best_weights if best_weights is not None else [1, 1]
                # Youden: weights[0]*sens + weights[1]*spec
                score = weights[0] * self.sensitivities + weights[1] * self.specificities
                idx = np.argmax(score)
            elif best_method == "closest.topleft":
                weights = best_weights if best_weights is not None else [1, 1]
                # Dist to (0, 100) or (0, 1)
                # R distance: sqrt( (weights[0]*fpr)^2 + (weights[1]*(1-tpr))^2 )
                fpr = 100 - self.specificities if self.percent else 1 - self.specificities
                tpr = self.sensitivities / 100 if self.percent else self.sensitivities
                dist = np.sqrt((weights[0] * fpr)**2 + (weights[1] * (1 - tpr))**2)
                idx = np.argmin(dist)
            else:
                idx = 0
        elif input == "threshold" and isinstance(x, (int, float)):
            idx = np.argmin(np.abs(self.thresholds - x))
        elif input == "sensitivity" or input == "se":
            val = x if self.percent else x * 100 # Input is usually expected in percent
            idx = np.argmin(np.abs(self.sensitivities - val))
        elif input == "specificity" or input == "sp":
            val = x if self.percent else x * 100
            idx = np.argmin(np.abs(self.specificities - val))
        elif x == "all":
            # Return all as a DataFrame
            df = pd.DataFrame({
                'threshold': self.thresholds,
                'specificity': self.specificities,
                'sensitivity': self.sensitivities
            })
            if ret == "all":
                # Calculate additional metrics for all
                # Accuracy = (TP+TN)/Total
                # precision = TP/(TP+FP)
                # recall = sensitivity
                tpr = self.sensitivities / scale
                fpr = (100 - self.specificities) / scale if self.percent else 1 - self.specificities
                
                # Approximate accuracy: (TP + TN) / N = (TPR*P + TNR*(1-P))
                p = np.mean(self.response == 1)
                df['accuracy'] = (tpr * p + (self.specificities/scale) * (1-p)) * scale
                
                # Precision = TP / (TP + FP) = (TPR*P) / (TPR*P + FPR*(1-P))
                denom = (tpr * p + fpr * (1-p))
                df['precision'] = np.divide(tpr * p, denom, out=np.zeros_like(tpr), where=denom!=0) * scale
                df['recall'] = self.sensitivities
                df['tpr'] = tpr * scale
                df['fpr'] = fpr * scale
                return df
            elif isinstance(ret, str):
                return df[[ret]] if ret in df.columns else df
            elif isinstance(ret, list):
                return df[ret]
            return df
        else:
            idx = 0

        # Single point return
        res = {
            'threshold': self.thresholds[idx],
            'specificity': self.specificities[idx],
            'sensitivity': self.sensitivities[idx]
        }
        
        # Calculate metrics for 'best' or single threshold
        tp = np.sum(((self.marker >= res['threshold']) == 1) & (self.response == 1))
        fp = np.sum(((self.marker >= res['threshold']) == 1) & (self.response == 0))
        fn = np.sum(((self.marker >= res['threshold']) == 0) & (self.response == 1))
        tn = np.sum(((self.marker >= res['threshold']) == 0) & (self.response == 0))
        
        res['accuracy'] = ((tp + tn) / len(self.response)) * scale
        res['precision'] = (tp / (tp + fp) if (tp + fp) > 0 else 0) * scale
        res['recall'] = (tp / (tp + fn) if (tp + fn) > 0 else 0) * scale
        res['tpr'] = res['sensitivity']
        res['fpr'] = 100 - res['specificity'] if self.percent else 1 - res['specificity']
        res['tnr'] = res['specificity']
        res['fnr'] = 100 - res['recall'] if self.percent else 1 - res['recall']
        
        if ret == "all":
            return pd.Series(res)
        elif isinstance(ret, list):
            return pd.Series({k: res[k] for k in ret if k in res})
        elif isinstance(ret, str):
            return pd.Series({ret: [res[ret]]}) if ret in res else pd.Series()
        
        return pd.Series(res)

def roc(response, marker, percent=False):
    return pROC_ROC(response, marker, percent)

def smooth(roc_obj):
    # pROC smooth is a kernel density estimate of the ROC.
    # We'll return the same object as a placeholder since the example just calls coords on it.
    return roc_obj

# Main script
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
print(roc_s100b.coords(0.55).to_frame().T)

# Get the coordinates at 50% sensitivity
print(roc_s100b.coords(x=50, input="sensitivity").to_frame().T)
# Can be abbreviated:
print(roc_s100b.coords(50, "se").to_frame().T)

# Works with smoothed ROC curves
print(smooth(roc_s100b).coords(90, "specificity").to_frame().T)

# Get the sensitivities for all thresholds
cc = roc_s100b.coords("all", ret="sensitivity")
print(cc['sensitivity'].values)

# Get the best threshold
print(roc_s100b.coords("best", ret="threshold").to_frame().T)

# Get the best threshold according to different methods
roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)
print(roc_ndka.coords("best", ret="threshold", best_method="youden").to_frame().T)
print(roc_ndka.coords("best", ret="threshold", best_method="closest.topleft").to_frame().T)

# and with different weights
print(roc_ndka.coords("best", ret="threshold", best_method="youden", best_weights=[50, 0.2]).to_frame().T)
print(roc_ndka.coords("best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]).to_frame().T)

# This is available with the plot.roc function too:
# Mocking the print.thres plot
print("Plotting roc.ndka with best threshold...")

# Return more values:
print(roc_s100b.coords("best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]).to_frame().T)

# Return all values
print(roc_s100b.coords("best", ret="all").to_frame().T)

# Sensitivity + specificity vs cut-off diagram
df_all_ndka = roc_ndka.coords("all")
plt.figure()
plt.plot(df_all_ndka['threshold'], df_all_ndka['specificity'] + df_all_ndka['sensitivity'])
plt.xscale('log')
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# Plot the Precision-Recall curve
df_pr_ndka = roc_ndka.coords("all", ret=["recall", "precision"])
plt.figure()
plt.plot(df_pr_ndka['recall'], df_pr_ndka['precision'])
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# Alternatively plot the curve with TPR and FPR
df_tpr_fpr = roc_ndka.coords("all", ret=["tpr", "fpr"])
plt.figure()
plt.plot(df_tpr_fpr['fpr'], df_tpr_fpr['tpr'])
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()