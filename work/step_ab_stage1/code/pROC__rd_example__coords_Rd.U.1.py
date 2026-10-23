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

def get_roc_df(outcome, score):
    fpr, tpr, thresholds = roc_curve(outcome, score)
    # pROC's roc() result stores sensitivities and specificities.
    # thresholds in sklearn are sorted descending. 
    # We create a dataframe that mimics pROC's coords behavior.
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * 100,
        'specificity': (1 - fpr) * 100,
        'tpr': tpr * 100,
        'fpr': fpr * 100
    })
    return df

# Create a ROC curve:
roc_s100b = get_roc_df(aSAH['outcome'], aSAH['s100b'])

# Get the coordinates of S100B threshold 0.55
# In R, coords(roc, 0.55) returns the point where threshold is 0.55
coords_055 = roc_s100b[roc_s100b['threshold'] == 0.55]
print(coords_055)

# Get the coordinates at 50% sensitivity
# x=50, input="sensitivity"
idx_se50 = (np.abs(roc_s100b['sensitivity'] - 50)).idxmin()
coords_se50 = roc_s100b.loc[[idx_se50]]
print(coords_se50)

# Abbreviated call
coords_se50_abbr = roc_s100b.loc[[idx_se50]]
print(coords_se50_abbr)

# Works with smoothed ROC curves
# Simple linear interpolation for "smoothing" approximation
f_spec = interp1d(roc_s100b['specificity'], roc_s100b['threshold'], fill_value="extrapolate")
coords_smooth = f_spec(90)
print(coords_smooth)

# Get the sensitivities for all thresholds
cc = roc_s100b[['sensitivity']]
print(cc['sensitivity'])

# Get the best threshold (Youden's J: sens + spec - 100)
youden_s100b = roc_s100b['sensitivity'] + roc_s100b['specificity'] - 100
best_idx_s100b = youden_s100b.idxmax()
coords_best_thresh = roc_s100b.loc[[best_idx_s100b], 'threshold']
print(coords_best_thresh)

# Get the best threshold according to different methods
roc_ndka = get_roc_df(aSAH['outcome'], aSAH['ndka'])

# youden
youden_ndka = roc_ndka['sensitivity'] + roc_ndka['specificity'] - 100
best_idx_ndka_youden = youden_ndka.idxmax()
coords_ndka_youden = roc_ndka.loc[[best_idx_ndka_youden], 'threshold']
print(coords_ndka_youden)

# closest.topleft: distance to (0, 100) in ROC space (FPR=0, TPR=100)
# Distance = sqrt(fpr^2 + (100-tpr)^2)
dist_topleft = np.sqrt(roc_ndka['fpr']**2 + (100 - roc_ndka['tpr'])**2)
best_idx_ndka_topleft = dist_topleft.idxmin()
coords_ndka_topleft = roc_ndka.loc[[best_idx_ndka_topleft], 'threshold']
print(coords_ndka_topleft)

# and with different weights
# youden weighted: w1*sens + w2*spec
w_youden_ndka = 50 * roc_ndka['sensitivity'] + 0.2 * roc_ndka['specificity']
coords_ndka_w_youden = roc_ndka.loc[[w_youden_ndka.idxmax()], 'threshold']
print(coords_ndka_w_youden)

# closest.topleft weighted: sqrt(w1*fpr^2 + w2*(100-tpr)^2)
w_dist_ndka = np.sqrt(5 * roc_ndka['fpr']**2 + 0.2 * (100 - roc_ndka['tpr'])**2)
coords_ndka_w_topleft = roc_ndka.loc[[w_dist_ndka.idxmin()], 'threshold']
print(coords_ndka_w_topleft)

# plot(roc.ndka, print.thres="best" ...)
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.title("ROC Curve ndka")
plt.xlabel("FPR")
plt.ylabel("TPR")
# The print.thres logic typically adds a point/text to the plot
plt.text(roc_ndka.loc[best_idx_ndka_youden, 'fpr'], roc_ndka.loc[best_idx_ndka_youden, 'tpr'], f"Best: {roc_ndka.loc[best_idx_ndka_youden, 'threshold']:.2f}")
plt.show()

# Return more values
best_t = roc_s100b.loc[best_idx_s10b := youden_s100b.idxmax(), 'threshold']
preds_s100b = (aSAH['s100b'] >= best_t).astype(int)
coords_best_multi = pd.DataFrame({
    'threshold': [best_t],
    'specificity': [roc_s100b.loc[best_idx_s10b, 'specificity']],
    'sensitivity': [roc_s100b.loc[best_idx_s10b, 'sensitivity']],
    'accuracy': [accuracy_score(aSAH['outcome'], preds_s100b) * 100],
    'precision': [precision_score(aSAH['outcome'], preds_s100b) * 100],
    'recall': [recall_score(aSAH['outcome'], preds_s100b) * 100]
})
print(coords_best_multi)

# Return all values
coords_best_all = roc_s100b.loc[[best_idx_s10b]]
print(coords_best_all)

# sensitivity + specificity vs. cut-off diagram
plt.figure()
plot_data_1 = roc_ndka.copy()
plot_data_1['sum_spec_sens'] = plot_data_1['specificity'] + plot_data_1['sensitivity']
valid_mask = np.isfinite(plot_data_1['threshold'])
plt.semilogx(plot_data_1.loc[valid_mask, 'threshold'], plot_data_1.loc[valid_mask, 'sum_spec_sens'])
plt.title("Spec + Sens vs Threshold")
plt.show()

# Plot the Precision-Recall curve
prec, rec, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec * 100, prec * 100)
plt.ylim(0, 100)
plt.title("Precision-Recall Curve")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.show()

# Alternatively plot the curve with TPR and FPR
plt.figure()
plt.plot(roc_ndka['fpr'], roc_ndka['tpr'])
plt.title("TPR vs FPR")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.show()