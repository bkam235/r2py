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
    # pROC roc() stores the object. We'll store as a dict/object
    multiplier = 100 if percent else 1
    return {
        'response': response,
        'marker': marker,
        'fpr': fpr,
        'tpr': tpr,
        'thresholds': thresholds,
        'percent': percent,
        'multiplier': multiplier
    }

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    response = roc_obj['response']
    marker = roc_obj['marker']
    mult = roc_obj['multiplier']
    
    # If x is "best"
    if x == "best":
        fpr = roc_obj['fpr']
        tpr = roc_obj['tpr']
        thresholds = roc_obj['thresholds']
        
        if best_method == "youden":
            # Youden: Sens + Spec - 1 (or (Sens + Spec - 100) if percent)
            # With weights: w1*sens + w2*spec
            w1, w2 = (best_weights if best_weights is not None else (1, 1))
            # Using scaled values (0-1) for the calculation
            j_stat = w1 * tpr + w2 * (1 - fpr)
            idx = np.argmax(j_stat)
        elif best_method == "closest.topleft":
            # Distance to (0, 1)
            w1, w2 = (best_weights if best_weights is not None else (1, 1))
            dist = np.sqrt((w1 * fpr)**2 + (w2 * (1 - tpr))**2)
            idx = np.argmin(dist)
        else:
            idx = 0
            
        x = thresholds[idx]

    # Determine threshold value based on input
    thresh_val = None
    if input == "threshold":
        thresh_val = x
    elif input == "sensitivity" or input == "se":
        # Find threshold where sensitivity (tpr * mult) is closest to x
        tprs = roc_obj['tpr'] * mult
        idx = np.argmin(np.abs(tprs - x))
        thresh_val = roc_obj['thresholds'][idx]
    elif input == "specificity" or input == "sp":
        specs = (1 - roc_obj['fpr']) * mult
        idx = np.argmin(np.abs(specs - x))
        thresh_val = roc_obj['thresholds'][idx]

    if x == "all":
        # Generate a dataframe of all coordinates
        fpr = roc_obj['fpr']
        tpr = roc_obj['tpr']
        thresholds = roc_obj['thresholds']
        
        df = pd.DataFrame({
            'threshold': thresholds,
            'sensitivity': tpr * mult,
            'specificity': (1 - fpr) * mult,
            'tpr': tpr * 100,
            'fpr': fpr * 100
        })
        
        # Calculate precision, recall, accuracy for all
        # Note: This can be slow for large datasets
        precisions = []
        recalls = []
        accuracies = []
        for t in thresholds:
            preds = (marker >= t).astype(int)
            precisions.append(precision_score(response, preds, zero_division=0) * mult)
            recalls.append(recall_score(response, preds, zero_division=0) * mult)
            accuracies.append(accuracy_score(response, preds) * mult)
        
        df['precision'] = precisions
        df['recall'] = recalls
        df['accuracy'] = accuracies
        
        if isinstance(ret, str):
            if ret == "all": return df
            return df[[ret]] if ret in df.columns else df
        elif isinstance(ret, list):
            return df[ret]
        return df

    # Single threshold case
    preds = (marker >= thresh_val).astype(int)
    res = {
        'threshold': thresh_val,
        'sensitivity': recall_score(response, preds, zero_division=0) * mult,
        'specificity': (1 - (np.sum((preds == 1) & (response == 0)) / np.sum(response == 0) if np.sum(response == 0) > 0 else 0)) * mult,
        'accuracy': accuracy_score(response, preds) * mult,
        'precision': precision_score(response, preds, zero_division=0) * mult,
        'recall': recall_score(response, preds, zero_division=0) * mult,
        'tpr': recall_score(response, preds, zero_division=0) * 100,
        'fpr': (np.sum((preds == 1) & (response == 0)) / np.sum(response == 0) if np.sum(response == 0) > 0 else 0) * 100
    }
    
    if isinstance(ret, str):
        if ret == "all": return pd.Series(res)
        return pd.Series({ret: res[ret]}) if ret in res else pd.Series()
    elif isinstance(ret, list):
        return pd.Series({k: res[k] for k in ret})
    
    return pd.Series(res)

def smooth(roc_obj):
    # Simplified smoothing: essentially just returning the same object for this example
    return roc_obj

# Create a ROC curve:
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
coords(roc_s100b, 0.55)

# Get the coordinates at 50% sensitivity
coords(roc=roc_s100b, x=50, input="sensitivity")
# Can be abbreviated:
coords(roc_s100b, 50, "se")

# Works with smoothed ROC curves
coords(smooth(roc_s100b), 90, "specificity")

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
coords(roc_s100b, "best", ret="threshold")

# Get the best threshold according to different methods
roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)
coords(roc_ndka, "best", ret="threshold", 
       best_method="youden") # default
coords(roc_ndka, "best", ret="threshold", 
       best_method="closest.topleft")

# and with different weights
coords(roc_ndka, "best", ret="threshold", 
       best_method="youden", best_weights=np.array([50, 0.2]))
coords(roc_ndka, "best", ret="threshold", 
       best_method="closest.topleft", best_weights=np.array([5, 0.2]))
       
# This is available with the plot.roc function too (Simulated)
print("Plotting ROC for ndka...")

# Return more values:
coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy",
                           "precision", "recall"])

# Return all values
coords(roc_s100b, "best", ret = "all")
                           
# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
all_coords_ndka = coords(roc_ndka, "all")
plot_data_1 = all_coords_ndka.copy()
plot_data_1['sum_spec_sens'] = plot_data_1['specificity'] + plot_data_1['sensitivity']
plt.figure()
plt.semilogx(plot_data_1['threshold'], plot_data_1['sum_spec_sens'])
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')

# Plot the Precision-Recall curve
pr_coords_ndka = coords(roc_ndka, "all", ret = ["recall", "precision"])
plt.figure()
plt.plot(pr_coords_ndka['recall'], pr_coords_ndka['precision'])
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
tpr_fpr_coords_ndka = coords(roc_ndka, "all", ret = ["tpr", "fpr"])
plt.figure()
plt.plot(tpr_fpr_coords_ndka['fpr'], tpr_fpr_coords_ndka['tpr'])
plt.xlabel('fpr')
plt.ylabel('tpr')