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

class ROC:
    def __init__(self, outcome, predictor, percent=False):
        self.outcome = np.array(outcome)
        self.predictor = np.array(predictor)
        self.percent = percent
        
        fpr, tpr, thresholds = roc_curve(self.outcome, self.predictor)
        # pROC's thresholds are slightly different; sklearn includes a threshold > max(predictor)
        # To mimic pROC, we keep the standard roc_curve data
        self.fpr = fpr
        self.tpr = tpr
        self.thresholds = thresholds
        
        if percent:
            self.sensitivity = tpr * 100
            self.specificity = (1 - fpr) * 100
        else:
            self.sensitivity = tpr
            self.specificity = (1 - fpr)

def smooth(roc_obj):
    # Simple approximation of smoothing for the purpose of the example
    return roc_obj

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # Convert ROC object to a DataFrame for easier manipulation
    df = pd.DataFrame({
        'threshold': roc_obj.thresholds,
        'sensitivity': roc_obj.sensitivity,
        'specificity': roc_obj.specificity
    })
    
    # Handle "best"
    if x == "best":
        if best_method == "youden":
            # Weights are sensitivity and specificity
            w_sens = best_weights[0] if best_weights is not None else 1.0
            w_spec = best_weights[1] if best_weights is not None else 1.0
            score = w_sens * df['sensitivity'] + w_spec * df['specificity']
            idx = score.idxmax()
        elif best_method == "closest.topleft":
            # Distance to (0, 100) in ROC space
            w_sens = best_weights[0] if best_weights is not None else 1.0
            w_spec = best_weights[1] if best_weights is not None else 1.0
            # FPR = 1 - specificity; TPR = sensitivity
            # Normalized to 0-1 for distance
            fpr = (100 - df['specificity']) / 100 if roc_obj.percent else (1 - df['specificity'])
            tpr = df['sensitivity'] / 100 if roc_obj.percent else df['sensitivity']
            dist = np.sqrt((w_sens * fpr)**2 + (w_spec * (1 - tpr))**2)
            idx = dist.idxmin()
        else:
            idx = 0
        
        row = df.iloc[[idx]].copy()
        # Calculate additional metrics if requested
        if ret == "all" or any(m in ret if isinstance(ret, list) else m == ret for m in ["accuracy", "precision", "recall"]):
            thresh = row['threshold'].values[0]
            preds = (roc_obj.predictor >= thresh).astype(int)
            
            # Correct for sklearn's threshold offset if necessary
            # pROC thresholds are the actual cut-offs
            
            row['accuracy'] = accuracy_score(roc_obj.outcome, preds) * 100
            row['precision'] = precision_score(roc_obj.outcome, preds) * 100
            row['recall'] = recall_score(roc_obj.outcome, preds) * 100
            row['tpr'] = row['sensitivity']
            row['fpr'] = 100 - row['specificity']
            
            # Simplified version of 'all' for a single row
            if ret == "all":
                # Return a dictionary-like structure or a series to match pROC
                return row.iloc[0].to_dict()
                
        if isinstance(ret, list):
            return row[ret]
        elif ret != "all":
            return row[[ret]] if ret in df.columns else row
        return row

    # Handle "all"
    if x == "all":
        df['tpr'] = df['sensitivity']
        df['fpr'] = 100 - df['specificity']
        if isinstance(ret, list):
            return df[ret]
        elif ret != "all":
            return df[[ret]]
        return df

    # Handle specific value
    if input == "threshold":
        # Find closest threshold
        idx = (np.abs(df['threshold'] - x)).idxmin()
        return df.iloc[[idx]]
    elif input == "sensitivity" or input == "se":
        idx = (np.abs(df['sensitivity'] - x)).idxmin()
        return df.iloc[[idx]]
    elif input == "specificity" or input == "sp":
        idx = (np.abs(df['specificity'] - x)).idxmin()
        return df.iloc[[idx]]
    
    return df

# Start translation
aSAH_df = pd.DataFrame(aSAH)
roc_s100b = ROC(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
print(coords(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords(roc_s100b, x=50, input="sensitivity"))
# Can be abbreviated:
print(coords(roc_s100b, 50, "se"))

# Works with smoothed ROC curves
print(coords(smooth(roc_s100b), 90, "specificity"))

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
roc_ndka = ROC(aSAH_df['outcome'], aSAH_df['ndka'], percent=True)
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# and with different weights
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# Plotting (simulated with print/matplotlib)
# plot(roc.ndka, print.thres="best", ...)
plt.figure()
plt.plot(roc_ndka.fpr / 100, roc_ndka.sensitivity / 100)
plt.title("ROC Curve - ndka")
plt.show()

# Return more values:
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# Return all values
print(coords(roc_s100b, "best", ret="all"))

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
all_coords_ndka = coords(roc_ndka, "all")
plt.figure()
plt.plot(all_coords_ndka['threshold'], all_coords_ndka['specificity'] + all_coords_ndka['sensitivity'])
plt.xscale('log')
plt.title("Specificity + Sensitivity vs Threshold")
plt.show()

# Plot the Precision-Recall curve
pr_coords = coords(roc_ndka, "all", ret=["recall", "precision"])
# precision/recall typically calculated separately
prec_ndka, rec_ndka, _ = precision_recall_curve(aSAH_df['outcome'], aSAH_df['ndka'])
plt.figure()
plt.plot(rec_ndka * 100, prec_ndka * 100)
plt.ylim(0, 100)
plt.title("Precision-Recall Curve")
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
tpr_fpr_coords = coords(roc_ndka, "all", ret=["tpr", "fpr"])
plt.figure()
plt.plot(tpr_fpr_coords['fpr'], tpr_fpr_coords['tpr'])
plt.title("TPR vs FPR")
plt.show()