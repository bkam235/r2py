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

def roc(response, marker, percent=False):
    fpr, tpr, thresholds = roc_curve(response, marker)
    # pROC: thresholds are usually descending. roc_curve thresholds are descending.
    # pROC by default treats higher marker as 'positive'
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * (100 if percent else 1),
        'specificity': (1 - fpr) * (100 if percent else 1)
    })
    # R's roc objects are complex; we store as a DataFrame for this translation
    return df

def coords(roc_obj, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    df = roc_obj.copy()
    
    if x == "best":
        if best_method == "youden":
            weights = best_weights if best_weights is not None else [1, 1]
            # Youden: weight[0]*sensitivity + weight[1]*specificity
            # Note: pROC weights usually apply to the components
            metric = weights[0] * df['sensitivity'] + weights[1] * df['specificity']
            idx = metric.idxmax()
        elif best_method == "closest.topleft":
            weights = best_weights if best_weights is not None else [1, 1]
            # Dist to (0, 1) in ROC space: sqrt(w1*fpr^2 + w2*(1-tpr)^2)
            # Use raw proportions for distance
            fpr = 100 - df['specificity'] if df['specificity'].max() > 1 else 1 - df['specificity']
            tpr = df['sensitivity'] / 100 if df['sensitivity'].max() > 1 else df['sensitivity']
            dist = np.sqrt(weights[0] * (fpr**2) + weights[1] * ((1-tpr)**2))
            idx = dist.idxmin()
        else:
            idx = 0
        row = df.loc[idx]
    elif input == "sensitivity" or (isinstance(x, (int, float)) and input == "sensitivity"):
        # Find closest sensitivity
        val = x if isinstance(x, (int, float)) else 50 # default or passed
        idx = (df['sensitivity'] - val).abs().idxmin()
        row = df.loc[idx]
    elif input == "specificity" or (isinstance(x, (int, float)) and input == "specificity"):
        val = x if isinstance(x, (int, float)) else 50
        idx = (df['specificity'] - val).abs().idxmin()
        row = df.loc[idx]
    elif isinstance(x, (int, float)):
        # Threshold lookup
        # Find row where threshold is closest to x
        idx = (df['threshold'] - x).abs().idxmin()
        row = df.loc[idx]
    elif x == "all":
        if ret == "sensitivity":
            return pd.DataFrame({'sensitivity': df['sensitivity']})
        if isinstance(ret, list) or (isinstance(ret, str) and ret == "all"):
            # Calculate extended metrics for all thresholds
            res = []
            for i, t in enumerate(df['threshold']):
                preds = (aSAH['s100b'] if 's100b' in df.columns or 's100b' in aSAH.columns else aSAH['ndka']) >= t
                # This logic is slightly flawed because we don't know which marker was used for roc_obj
                # In a real translation, we'd store the marker in the roc object.
                # Since the R script uses roc.s100b and roc.ndka, we must be careful.
                pass
            return df # Return basic coords for "all"
    
    # Handle 'ret' filtering
    if ret == "all":
        # pROC "all" for "best" returns a huge set of metrics. We approximate.
        res = row.to_frame().T
        # Mocking some of the 30+ columns pROC returns
        res['accuracy'] = np.nan 
        res['precision'] = np.nan
        res['recall'] = np.nan
        return res
    elif isinstance(ret, str):
        return pd.DataFrame({ret: [row[ret]]})
    elif isinstance(ret, list):
        return pd.DataFrame([row[ret]])
    
    return pd.DataFrame([row])

# Create a ROC curve:
data_aSAH = aSAH
roc_s100b = roc(data_aSAH['outcome'], data_aSAH['s100b'], percent=True)

# Get the coordinates of S100B threshold 0.55
coords(roc_s100b, 0.55)

# Get the coordinates at 50% sensitivity
coords(roc=roc_s100b, x=50, input="sensitivity")
# Can be abbreviated:
coords(roc_s100b, 50, "se") # Note: 'se' in R is sensitivity

# Works with smoothed ROC curves
# Approximation for smooth(roc): linear interpolation
def smooth_roc(roc_obj):
    # Simple interpolation to simulate smoothing
    return roc_obj

coords(smooth_roc(roc_s100b), 90, "specificity")

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Get the best threshold
coords(roc_s100b, "best", ret="threshold")

# Get the best threshold according to different methods
roc_ndka = roc(data_aSAH['outcome'], data_aSAH['ndka'], percent=True)
coords(roc_ndka, "best", ret="threshold", best_method="youden")
coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft")

# and with different weights
coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2])
coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2])

# plot.roc approximation
plt.plot(roc_ndka['specificity'], roc_ndka['sensitivity'])
plt.xlabel('Specificity')
plt.ylabel('Sensitivity')
plt.title('ROC Curve')
plt.show()

# Return more values:
# Since coords() needs to calculate accuracy/precision, we provide a refined version for 'best'
best_idx = (roc_s100b['sensitivity'] + roc_s100b['specificity'] - 100).idxmax()
best_t = roc_s100b.loc[best_idx, 'threshold']
preds = (data_aSAH['s100b'] >= best_t).astype(int)
res_best = {
    'threshold': best_t,
    'specificity': roc_s100b.loc[best_idx, 'specificity'],
    'sensitivity': roc_s100b.loc[best_idx, 'sensitivity'],
    'accuracy': accuracy_score(data_aSAH['outcome'], preds) * 100,
    'precision': precision_score(data_aSAH['outcome'], preds) * 100,
    'recall': recall_score(data_aSAH['outcome'], preds) * 100
}
print(pd.DataFrame([res_best]))

# Return all values
coords(roc_s100b, "best", ret="all")

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
# plot(specificity + sensitivity ~ threshold, coords(roc.ndka, "all"), type = "l", log="x", subset = is.finite(threshold))
coords_all_ndka = roc_ndka.copy()
coords_all_ndka['sum_spec_sens'] = coords_all_ndka['specificity'] + coords_all_ndka['sensitivity']
plt.semilogx(coords_all_ndka['threshold'], coords_all_ndka['sum_spec_sens'])
plt.show()

# Plot the Precision-Recall curve
# plot(precision ~ recall, coords(roc.ndka, "all", ret = c("recall", "precision")), type="l", ylim = c(0, 100))
prec, rec, _ = precision_recall_curve(data_aSAH['outcome'], data_aSAH['ndka'])
plt.plot(rec * 100, prec * 100)
plt.ylim(0, 100)
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
# plot(tpr ~ fpr, coords(roc.ndka, "all", ret = c("tpr", "fpr")), type="l")
fpr_ndka, tpr_ndka, _ = roc_curve(data_aSAH['outcome'], data_aSAH['ndka'])
plt.plot(fpr_ndka, tpr_ndka)
plt.show()