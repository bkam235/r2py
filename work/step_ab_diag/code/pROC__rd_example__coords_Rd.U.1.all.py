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
    mult = 100 if percent else 1
    # pROC stores thresholds and corresponding metrics. 
    # Note: sklearn's thresholds[0] is always Max(marker)+1.
    # pROC's roc object structure:
    return {
        'response': response,
        'marker': marker,
        'thresholds': thresholds,
        'tpr': tpr * mult,
        'fpr': fpr * mult,
        'sensitivity': tpr * mult,
        'specificity': (1 - fpr) * mult,
        'percent': percent
    }

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    tpr = roc_obj['sensitivity']
    spec = roc_obj['specificity']
    thres = roc_obj['thresholds']
    
    if x == "best":
        if best_method == "youden":
            # Youden's J = sens + spec - 100 (if percent=True)
            score = tpr + spec - (100 if roc_obj['percent'] else 1)
            if best_weights is not None:
                score = best_weights[0] * tpr + best_weights[1] * spec
            idx = np.argmax(score)
        elif best_method == "closest.topleft":
            # Distance to (0, 100) -> dist = sqrt((fpr/100)^2 + (1 - tpr/100)^2)
            fpr_val = roc_obj['fpr'] / (100 if roc_obj['percent'] else 1)
            tpr_val = roc_obj['tpr'] / (100 if roc_obj['percent'] else 1)
            dist = np.sqrt(fpr_val**2 + (1 - tpr_val)**2)
            if best_weights is not None:
                dist = np.sqrt(best_weights[0] * fpr_val**2 + best_weights[1] * (1 - tpr_val)**2)
            idx = np.argmin(dist)
        else:
            idx = 0
    elif input == "threshold" or (isinstance(x, (int, float, np.number))):
        # Find closest threshold to x
        idx = np.argmin(np.abs(thres - x))
    elif input == "sensitivity" or x == "se":
        # Find threshold for target sensitivity
        target = x if isinstance(x, (int, float)) else 50
        idx = np.argmin(np.abs(tpr - target))
    elif input == "specificity" or x == "sp":
        target = x if isinstance(x, (int, float)) else 50
        idx = np.argmin(np.abs(spec - target))
    else:
        # "all" case
        if ret == "all":
            return pd.DataFrame({'threshold': thres, 'specificity': spec, 'sensitivity': tpr})
        elif isinstance(ret, str):
            return pd.DataFrame({ret: (tpr if ret == "sensitivity" else spec if ret == "specificity" else thres)})
        elif isinstance(ret, list):
            res = {}
            for r in ret:
                if r == "sensitivity": res['sensitivity'] = tpr
                elif r == "specificity": res['specificity'] = spec
                elif r == "threshold": res['threshold'] = thres
                elif r == "tpr": res['tpr'] = tpr
                elif r == "fpr": res['fpr'] = roc_obj['fpr']
            return pd.DataFrame(res)
        return pd.DataFrame()

    # Single point return
    best_t = thres[idx]
    # Calculate metrics for a single threshold
    preds = (roc_obj['marker'] >= best_t).astype(int)
    # Correct for cases where threshold is slightly off due to sklearn's max+1
    # but R's pROC handles thresholds by treating them as cut-offs.
    # We simulate the coords output format.
    
    # Calculate actual metrics based on this specific threshold
    tp = np.sum((preds == 1) & (roc_obj['response'] == 1))
    fn = np.sum((preds == 0) & (roc_obj['response'] == 1))
    tn = np.sum((preds == 0) & (roc_obj['response'] == 0))
    fp = np.sum((preds == 1) & (roc_obj['response'] == 0))
    
    sens = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 0
    spec_val = (tn / (tn + fp) * 100) if (tn + fp) > 0 else 0
    acc = ((tp + tn) / (tp + tn + fp + fn) * 100) if (tp + tn + fp + fn) > 0 else 0
    prec = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0
    rec = sens
    
    full_metrics = {
        'threshold': best_t, 'specificity': spec_val, 'sensitivity': sens,
        'accuracy': acc, 'precision': prec, 'recall': rec,
        'tn': tn, 'tp': tp, 'fn': fn, 'fp': fp,
        'npv': (tn / (tn + fn) * 100) if (tn + fn) > 0 else 0,
        'ppv': prec, 'fdr': (fp / (fp + tp) * 100) if (fp + tp) > 0 else 0,
        'fpr': (fp / (fp + tn) * 100) if (fp + tn) > 0 else 0,
        'tpr': sens, 'tnr': spec_val, 'fnr': (fn / (fn + tp) * 100) if (fn + tp) > 0 else 0,
        '1-specificity': (fp / (fp + tn) * 100) if (fp + tn) > 0 else 0,
        '1-sensitivity': (fn / (fn + tp) * 100) if (fn + tp) > 0 else 0,
        '1-accuracy': 100 - acc, '1-npv': 100 - (tn / (tn + fn) * 100 if (tn + fn) > 0 else 0),
        '1-ppv': 100 - prec, 'lr_pos': (sens / (100 - spec_val)) if spec_val < 100 else np.inf,
        'lr_neg': ((100 - sens) / (100 - (100 - spec_val))) if (100 - spec_val) > 0 else np.inf,
        'youden': sens + spec_val - 100, 'closest.topleft': np.sqrt((fp/(fp+tn))**2 + (fn/(fn+tp))**2)
    }
    
    if ret == "all":
        return pd.DataFrame([full_metrics], index=['threshold'])
    elif isinstance(ret, list):
        return pd.DataFrame([ {k: v for k, v in full_metrics.items() if k in ret} ], index=['threshold'])
    elif ret == "threshold":
        return pd.DataFrame({'threshold': [best_t]})
    else:
        # default coords return threshold, specificity, sensitivity
        return pd.DataFrame({'threshold': [best_t], 'specificity': [spec_val], 'sensitivity': [sens]})

# Mock smooth function
def smooth(roc_obj):
    # For this example, smoothing isn't strictly implemented, return original
    return roc_obj

# --- Main Execution ---
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
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# and with different weights
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# plot(roc.ndka, ...)
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

# Return more values:
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# Return all values
print(coords(roc_s100b, "best", ret="all"))

# Sensitivity + Specificity vs. cut-off
all_coords = coords(roc_ndka, "all")
plt.figure()
plt.plot(all_coords['threshold'], all_coords['specificity'] + all_coords['sensitivity'])
plt.xscale('log')
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# Precision-Recall curve
pr_coords = coords(roc_ndka, "all", ret=["recall", "precision"])
# Note: pROC's 'all' for precision/recall is tricky. In R, it's computed. 
# In our simulation, we use sklearn's PR curve for the plot.
p, r, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(r * 100, p * 100)
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# TPR and FPR
tpr_fpr_coords = coords(roc_ndka, "all", ret=["tpr", "fpr"])
plt.figure()
plt.plot(tpr_fpr_coords['fpr'], tpr_fpr_coords['tpr'])
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()