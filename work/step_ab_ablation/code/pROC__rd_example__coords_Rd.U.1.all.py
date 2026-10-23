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

def get_roc_df(outcome, predictor):
    # sklearn.metrics.roc_curve returns fpr, tpr, thresholds
    # thresholds[0] is often a dummy value (max(predictor) + 1)
    fpr, tpr, thresholds = roc_curve(outcome, predictor)
    
    # pROC uses 0-100 scale for percent=TRUE
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * 100,
        'specificity': (1 - fpr) * 100
    })
    # Remove the dummy threshold at index 0 that sklearn adds
    df = df.iloc[1:].reset_index(drop=True)
    return df

def coords(roc_df, x=None, input_type="threshold", ret="all", best_method="youden", best_weights=None):
    # Handle "best"
    if x == "best":
        if best_method == "youden":
            # Youden = Sens + Spec - 100
            weights = best_weights if best_weights else [1.0, 1.0]
            score = weights[0] * roc_df['sensitivity'] + weights[1] * roc_df['specificity']
            idx = score.idxmax()
        elif best_method == "closest.topleft":
            # Distance to (0, 100) in ROC space (FPR=0, TPR=100)
            # FPR = 100 - Specificity
            weights = best_weights if best_weights else [1.0, 1.0]
            dist = np.sqrt(weights[0] * (100 - roc_df['specificity'])**2 + weights[1] * (100 - roc_df['sensitivity'])**2)
            idx = dist.idxmin()
        
        row = roc_df.loc[[idx]]
        # Calculate additional metrics if requested
        if ret == "all" or any(m in ret for m in ["accuracy", "precision", "recall"]):
            t = row['threshold'].values[0]
            # Re-calculate based on original data provided in the outer scope
            # This assumes aSAH and the predictor are available
            # In this specific script, the predictor varies (s100b vs ndka)
            # Since we can't pass the predictor here easily, we'll use a global or the logic from the main flow
            pass 
        
        if ret == "threshold": return row[['threshold']]
        if ret == "sensitivity": return row[['sensitivity']]
        if ret == "specificity": return row[['specificity']]
        if ret == "all": return row
        if isinstance(ret, list):
            return row[ret]
        return row

    # Handle "all"
    if x == "all":
        if ret == "all": return roc_df
        if isinstance(ret, list): return roc_df[ret]
        return roc_df[[ret]]

    # Handle specific value (x)
    if input_type == "threshold":
        res = roc_df[roc_df['threshold'] == x]
        if res.empty:
            # Find closest if exact not found
            idx = (roc_df['threshold'] - x).abs().idxmin()
            res = roc_df.loc[[idx]]
        return res
    
    if input_type in ["sensitivity", "se"]:
        idx = (roc_df['sensitivity'] - x).abs().idxmin()
        return roc_df.loc[[idx]]
    
    if input_type in ["specificity", "sp"]:
        idx = (roc_df['specificity'] - x).abs().idxmin()
        return roc_df.loc[[idx]]

    return None

# Create ROC curves
roc_s100b = get_roc_df(aSAH['outcome'], aSAH['s100b'])
roc_ndka = get_roc_df(aSAH['outcome'], aSAH['ndka'])

# Coordinates for threshold 0.55
print(coords(roc_s100b, 0.55))

# Coordinates at 50% sensitivity
print(coords(roc_s100b, x=50, input_type="sensitivity"))
print(coords(roc_s100b, 50, "se"))

# Smoothed ROC approximation
# pROC smooth() uses kernel density. Here we use linear interpolation as a proxy for the coords lookup.
f_interp = interp1d(roc_s100b['specificity'], roc_s100b['sensitivity'], fill_value="extrapolate")
# coords(smooth(roc.s100b), 90, "specificity")
res_smooth = pd.DataFrame({'specificity': [90.0], 'sensitivity': [f_interp(90.0)]})
print(res_smooth)

# Sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'])

# Best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Best threshold for ndka
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# With different weights
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# plot(roc.ndka, ...) - simulate by plotting
plt.figure()
plt.plot(100 - roc_ndka['specificity'], roc_ndka['sensitivity'])
plt.xlabel('1 - Specificity')
plt.ylabel('Sensitivity')
plt.title('ROC Curve ndka')
plt.show()

# Return more values for s100b best
best_row = coords(roc_s100b, "best", ret="all")
best_t = best_row['threshold'].values[0]
preds = (aSAH['s100b'] >= best_t).astype(int)
metrics = {
    'threshold': best_t,
    'specificity': best_row['specificity'].values[0],
    'sensitivity': best_row['sensitivity'].values[0],
    'accuracy': accuracy_score(aSAH['outcome'], preds) * 100,
    'precision': precision_score(aSAH['outcome'], preds) * 100,
    'recall': recall_score(aSAH['outcome'], preds) * 100
}
print(pd.DataFrame([metrics]).set_index('threshold').T)

# Return all values for s100b best
# We mimic the extensive pROC output columns
best_idx = roc_s100b['sensitivity'] + roc_s100b['specificity'] - 100
best_idx = best_idx.idxmax()
full_best = roc_s100b.loc[[best_idx]].copy()
# Add more calculated fields to match pROC "all"
t = full_best['threshold'].values[0]
p_s100b = (aSAH['s100b'] >= t).astype(int)
tp = np.sum((p_s100b == 1) & (aSAH['outcome'] == 1))
tn = np.sum((p_s100b == 0) & (aSAH['outcome'] == 0))
fp = np.sum((p_s100b == 1) & (aSAH['outcome'] == 0))
fn = np.sum((p_s100b == 0) & (aSAH['outcome'] == 1))
full_best['accuracy'] = (tp + tn) / len(aSAH) * 100
full_best['precision'] = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
full_best['recall'] = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
full_best['tn'] = tn
full_best['tp'] = tp
full_best['fn'] = fn
full_best['fp'] = fp
print(full_best)

# Plot specificity + sensitivity vs threshold
plt.figure()
plot_df = roc_ndka.copy()
plot_df['sum'] = plot_df['specificity'] + plot_df['sensitivity']
plt.semilogx(plot_df['threshold'], plot_df['sum'])
plt.show()

# Plot Precision-Recall curve
precision_ndka, recall_ndka, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(recall_ndka * 100, precision_ndka * 100)
plt.ylim(0, 100)
plt.show()

# Plot TPR vs FPR
plt.figure()
plt.plot(100 - roc_ndka['specificity'], roc_ndka['sensitivity'])
plt.show()