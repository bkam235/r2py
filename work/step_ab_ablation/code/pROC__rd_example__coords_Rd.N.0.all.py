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

def roc(response, marker, percent=False):
    # pROC::roc creates a representation of the ROC curve
    # response: binary outcome, marker: continuous predictor
    fpr, tpr, thresholds = roc_curve(response, marker)
    
    # pROC's thresholds usually include the max value + eps to ensure TPR=0, FPR=0
    # We store the data in a structure that mimics the pROC object
    mult = 100 if percent else 1
    return {
        'response': np.array(response),
        'marker': np.array(marker),
        'fpr': fpr,
        'tpr': tpr,
        'thresholds': thresholds,
        'percent': percent,
        'mult': mult
    }

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # This function emulates pROC::coords
    res = roc_obj
    mult = res['mult']
    
    # Handle "best"
    if x == "best":
        if best_method == "youden":
            # Youden: sensitivity + specificity - 1
            # if weighted: w1 * sens + w2 * spec
            w_sens = best_weights[0] if best_weights is not None else 1.0
            w_spec = best_weights[1] if best_weights is not None else 1.0
            score = w_sens * res['tpr'] + w_spec * (1 - res['fpr'])
            idx = np.argmax(score)
        elif best_method == "closest.topleft":
            # Distance to (0, 1)
            w_fpr = best_weights[0] if best_weights is not None else 1.0
            w_tpr = best_weights[1] if best_weights is not None else 1.0
            dist = np.sqrt((w_fpr * res['fpr'])**2 + (w_tpr * (1 - res['tpr']))**2)
            idx = np.argmin(dist)
        
        # Extract the best point
        best_t = res['thresholds'][idx]
        best_se = res['tpr'][idx] * mult
        best_sp = (1 - res['fpr'][idx]) * mult
    elif input == "threshold":
        # Find threshold closest to x
        idx = np.argmin(np.abs(res['thresholds'] - x))
        best_t = res['thresholds'][idx]
        best_se = res['tpr'][idx] * mult
        best_sp = (1 - res['fpr'][idx]) * mult
    elif input in ["sensitivity", "se"]:
        # Find threshold where sensitivity is closest to x
        target_se = x / mult if res['percent'] else x
        idx = np.argmin(np.abs(res['tpr'] - target_se))
        best_t = res['thresholds'][idx]
        best_se = res['tpr'][idx] * mult
        best_sp = (1 - res['fpr'][idx]) * mult
    elif input in ["specificity", "sp"]:
        # Find threshold where specificity is closest to x
        target_sp = x / mult if res['percent'] else x
        idx = np.argmin(np.abs((1 - res['fpr']) - target_sp))
        best_t = res['thresholds'][idx]
        best_se = res['tpr'][idx] * mult
        best_sp = (1 - res['fpr'][idx]) * mult
    elif x == "all":
        # Return all coordinates
        df = pd.DataFrame({
            'threshold': res['thresholds'],
            'sensitivity': res['tpr'] * mult,
            'specificity': (1 - res['fpr']) * mult,
            'tpr': res['tpr'] * mult,
            'fpr': res['fpr'] * mult
        })
        # Compute precision, recall, accuracy for all
        # Note: This is computationally expensive, we do it if ret requires it
        if "precision" in str(ret) or "accuracy" in str(ret) or ret == "all":
            # Calculate for each threshold
            accs, precs, recs = [], [], []
            for t in res['thresholds']:
                preds = (res['marker'] >= t).astype(int)
                accs.append(accuracy_score(res['response'], preds) * mult)
                precs.append(precision_score(res['response'], preds, zero_division=0) * mult)
                recs.append(recall_score(res['response'], preds, zero_division=0) * mult)
            df['accuracy'] = accs
            df['precision'] = precs
            df['recall'] = recs
        
        if isinstance(ret, str) and ret != "all":
            return df[[ret]] if ret in df.columns else df
        return df

    # For "best" or specific threshold, return a row-like structure
    # Compute precision/recall/accuracy for this specific threshold
    preds = (res['marker'] >= best_t).astype(int)
    out = {
        'threshold': best_t,
        'sensitivity': best_se,
        'specificity': best_sp,
        'accuracy': accuracy_score(res['response'], preds) * mult,
        'precision': precision_score(res['response'], preds, zero_division=0) * mult,
        'recall': recall_score(res['response'], preds, zero_division=0) * mult,
        'tpr': best_se,
        'fpr': (1 - best_sp/mult) * mult if res['percent'] else (1 - best_sp/mult)
    }
    
    if isinstance(ret, list):
        return {k: out[k] for k in ret if k in out}
    elif isinstance(ret, str) and ret != "all":
        return {ret: out[ret]} if ret in out else out
    return out

# Create a ROC curve:
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
print(coords(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords(roc=roc_s100b, x=50, input="sensitivity"))
# Can be abbreviated:
print(coords(roc_s100b, 50, "se"))

# Works with smoothed ROC curves (Approximation: pROC's smooth is complex, we use raw for now)
print(coords(roc_s100b, 90, "specificity"))

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)
print(coords(roc_ndka, "best", ret="threshold", best_method="youden")) # default
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# and with different weights
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# This is available with the plot.roc function too:
# Mimicking plot(roc.ndka, print.thres="best", ...)
# In Python, we just calculate and print the threshold to simulate the plot annotation
best_t_plot = coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2])
print(f"Plot Threshold: {best_t_plot}")

# Return more values:
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# Return all values
print(coords(roc_s100b, "best", ret="all"))

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
all_coords_ndka = coords(roc_ndka, "all")
plt.figure()
plt.plot(all_coords_ndka['threshold'], all_coords_ndka['specificity'] + all_coords_ndka['sensitivity'])
plt.xscale('log')
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# Plot the Precision-Recall curve
pr_coords_ndka = coords(roc_ndka, "all", ret=["recall", "precision"])
plt.figure()
plt.plot(pr_coords_ndka['recall'], pr_coords_ndka['precision'])
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
tpr_fpr_coords_ndka = coords(roc_ndka, "all", ret=["tpr", "fpr"])
plt.figure()
plt.plot(tpr_fpr_coords_ndka['fpr'], tpr_fpr_coords_ndka['tpr'])
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()