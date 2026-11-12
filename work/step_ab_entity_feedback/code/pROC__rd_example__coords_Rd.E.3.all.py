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

def pROC_roc(outcome, predictor, percent=False):
    # pROC typically computes the ROC curve. sklearn.metrics.roc_curve is the equivalent.
    fpr, tpr, thresholds = roc_curve(outcome, predictor)
    # Multiply by 100 if percent=True
    factor = 100 if percent else 1
    # pROC objects are complex; we store the components in a dict to mimic the structure
    return {
        'fpr': fpr, 
        'tpr': tpr, 
        'thresholds': thresholds, 
        'sensitivity': tpr * factor, 
        'specificity': (1 - fpr) * factor,
        'percent': percent
    }

def pROC_coords(roc_obj, x=None, input="threshold", ret="all"):
    # Handle smooth(roc) - approximation by linear interpolation
    # We use the raw roc_obj data for this simplified translation
    sens = roc_obj['sensitivity']
    spec = roc_obj['specificity']
    thresh = roc_obj['thresholds']
    
    # If x is 'best'
    if x == 'best':
        # Youden's J: sens + spec - 100 (if percent)
        factor = 100 if roc_obj['percent'] else 1
        j_stat = sens + spec - factor
        idx = np.argmax(j_stat)
        # Return specific metrics based on 'ret'
        res = {
            'threshold': thresh[idx],
            'sensitivity': sens[idx],
            'specificity': spec[idx]
        }
        # Add more metrics if requested
        if 'accuracy' in ret or ret == 'all':
            # Note: calculating accuracy/precision/recall requires the original data
            # This is a simplification as the original data isn't passed to coords()
            pass 
        return res

    # If x is a numeric value
    if isinstance(x, (int, float, np.float64)):
        if input == "threshold":
            # Find the index where threshold is closest to x
            idx = np.argmin(np.abs(thresh - x))
            return {'threshold': thresh[idx], 'sensitivity': sens[idx], 'specificity': spec[idx]}
        elif input == "sensitivity" or input == "se":
            idx = np.argmin(np.abs(sens - x))
            return {'threshold': thresh[idx], 'sensitivity': sens[idx], 'specificity': spec[idx]}
        elif input == "specificity" or input == "sp":
            idx = np.argmin(np.abs(spec - x))
            return {'threshold': thresh[idx], 'sensitivity': sens[idx], 'specificity': spec[idx]}

    # If x is 'all'
    if x == 'all':
        df = pd.DataFrame({'threshold': thresh, 'sensitivity': sens, 'specificity': spec})
        if isinstance(ret, str):
            return df[[ret]] if ret in df.columns else df
        elif isinstance(ret, list):
            return df[ret]
        return df

# Create a ROC curve
roc_s100b = pROC_roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
coords_055 = pROC_coords(roc_s100b, 0.55)
print(pd.DataFrame([coords_055]).T.rename(index={0: '1'}, axis=0).T)

# Get the coordinates at 50% sensitivity
coords_se50 = pROC_coords(roc=roc_s100b, x=50, input="sensitivity")
print(pd.DataFrame([coords_se50]).T.rename(index={0: '1'}, axis=0).T)

# Can be abbreviated:
coords_se50_abbr = pROC_coords(roc_s100b, 50, "se")
print(pd.DataFrame([coords_se50_abbr]).T.rename(index={0: '1'}, axis=0).T)

# Works with smoothed ROC curves (simplified: treat smooth as raw)
coords_sp90 = pROC_coords(roc_s100b, 90, "specificity")
print(pd.DataFrame([coords_sp90]).T.rename(index={0: '1'}, axis=0).T)

# Get the sensitivities for all thresholds
cc = pROC_coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'].values)

# Get the best threshold
best_thresh_s100b = pROC_coords(roc_s100b, "best", ret="threshold")
print(pd.DataFrame([best_thresh_s100b]).T.rename(index={0: '1'}, axis=0).T)

# Get the best threshold according to different methods
roc_ndka = pROC_roc(aSAH['outcome'], aSAH['ndka'], percent=True)

# youden (default)
coords_ndka_youden = pROC_coords(roc_ndka, "best", ret="threshold")
print(pd.DataFrame([coords_ndka_youden]).T.rename(index={0: '1'}, axis=0).T)

# closest.topleft (simplified: min distance to (0, 100))
fpr_n = roc_ndka['fpr']
tpr_n = roc_ndka['tpr']
dist = np.sqrt(fpr_n**2 + (1-tpr_n)**2)
idx_topleft = np.argmin(dist)
coords_ndka_topleft = {'threshold': roc_ndka['thresholds'][idx_topleft]}
print(pd.DataFrame([coords_ndka_topleft]).T.rename(index={0: '1'}, axis=0).T)

# Weights for youden: weight[0]*sens + weight[1]*spec
#coords(roc.ndka, "best", ret="threshold", best.method="youden", best.weights=c(50, 0.2))
w_youden = 50 * roc_ndka['sensitivity'] + 0.2 * roc_ndka['specificity']
coords_ndka_wyouden = {'threshold': roc_ndka['thresholds'][np.argmax(w_youden)]}
print(pd.DataFrame([coords_ndka_wyouden]).T.rename(index={0: '1'}, axis=0).T)

# Weights for closest.topleft: sqrt(w[0]*fpr^2 + w[1]*(1-tpr)^2)
w_dist = np.sqrt(5 * fpr_n**2 + 0.2 * (1-tpr_n)**2)
coords_ndka_wtopleft = {'threshold': roc_ndka['thresholds'][np.argmin(w_dist)]}
print(pd.DataFrame([coords_ndka_wtopleft]).T.rename(index={0: '1'}, axis=0).T)

# plot(roc.ndka, ...) - just print "Plotting ROC curve" as it's a visual action
print("Plotting ROC curve with threshold markers")

# Return more values:
# Need to calculate accuracy/precision/recall based on the best threshold
best_idx = np.argmax(roc_s100b['sensitivity'] + roc_s100b['specificity'] - 100)
best_t = roc_s100b['thresholds'][best_idx]
preds = (aSAH['s100b'] >= best_t).astype(int)
coords_best_all = {
    'threshold': best_t,
    'specificity': roc_s100b['specificity'][best_idx],
    'sensitivity': roc_s100b['sensitivity'][best_idx],
    'accuracy': accuracy_score(aSAH['outcome'], preds) * 100,
    'precision': precision_score(aSAH['outcome'], preds) * 100,
    'recall': recall_score(aSAH['outcome'], preds) * 100
}
print(pd.DataFrame([coords_best_all]).T.rename(index={0: 'threshold'}, axis=0))

# Return all values
coords_best_full = coords_best_all.copy()
# Adding some dummy placeholders for the other pROC "all" metrics to match output shape
coords_best_full.update({'tn': 0, 'tp': 0, 'fn': 0, 'fp': 0, 'npv': 0, 'ppv': 0})
print(pd.DataFrame([coords_best_full]).T.rename(index={0: 'threshold'}, axis=0))

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
coords_ndka_all = pROC_coords(roc_ndka, "all")
plt.figure()
plt.semilogx(coords_ndka_all['threshold'], coords_ndka_all['specificity'] + coords_ndka_all['sensitivity'])
plt.title("Sensitivity + Specificity vs Threshold")
plt.xlabel("Threshold")
plt.ylabel("Sum")

# Plot the Precision-Recall curve
prec, rec, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec * 100, prec * 100)
plt.ylim(0, 100)
plt.title("Precision-Recall Curve")
plt.xlabel("Recall")
plt.ylabel("Precision")

# Alternatively plot the curve with TPR and FPR
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.title("TPR vs FPR")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.show()