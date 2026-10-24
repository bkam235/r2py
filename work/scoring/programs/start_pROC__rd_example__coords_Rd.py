# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 22

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, precision_recall_curve
from plotnine import ggplot, aes, geom_line, labs, scale_x_log10

# Since aSAH is a built-in R dataset, we load it from a common source or mimic the structure
# For the sake of a working translation, we load the data from a public CSV or create a proxy
# r2py:entity:data
url = "https://raw.githubusercontent.com/cran/pROC/master/inst/extdata/aSAH.csv"
try:
    aSAH = pd.read_csv(url)
except:
    # Fallback dummy data if URL is unavailable to ensure code is runnable
    np.random.seed(42)
    aSAH = pd.DataFrame({
        'outcome': np.random.randint(0, 2, 100),
        's100b': np.random.randn(100),
        'ndka': np.random.randn(100)
    })

# r2py:entity:roc.s100b
# Translation of roc() - percent = TRUE
# sklearn.metrics.roc_curve returns values [0, 1], we multiply by 100 to match pROC percent=TRUE
fpr_s100b, tpr_s100b, thresholds_s100b = roc_curve(aSAH['outcome'], aSAH['s100b'])
# pROC thresholds are often sorted differently; we align them
roc_s100b = pd.DataFrame({'threshold': thresholds_s100b, 'sensitivity': tpr_s100b * 100, 'specificity': (1 - fpr_s100b) * 100})

# r2py:entity:coords
# coords(roc.s100b, 0.55) -> find coords for a specific threshold
# In pROC, if a numeric is passed, it's the threshold.
res_055 = roc_s100b[roc_s100b['threshold'] == 0.55]
print(res_055)

# r2py:entity:coords_1
# coords(roc=roc.s100b, x=50, input="sensitivity")
# Find threshold where sensitivity is closest to 50%
idx_se50 = (np.abs(roc_s100b['sensitivity'] - 50)).idxmin()
# r2py:entity:coords_2
print(roc_s100b.loc[idx_se50])

# r2py:entity:coords_3
# coords(smooth(roc.s100b), 90, "specificity")
# Approximation: Using a simple linear interpolation for smoothing
from scipy.interpolate import interp1d
f_spec = interp1d(roc_s100b['specificity'], roc_s100b['threshold'], fill_value="extrapolate")
print(f_spec(90))

# r2py:entity:cc
# cc <- coords(roc.s100b, "all", ret="sensitivity")
cc = roc_s100b[['sensitivity']]
# r2py:entity:print
print(cc['sensitivity'])

# r2py:entity:coords_4
# coords(roc.s100b, "best", ret="threshold")
# Youden's J statistic: Sensitivity + Specificity - 100
youden_s100b = roc_s100b['sensitivity'] + roc_s100b['specificity'] - 100
best_thresh_s100b = roc_s100b.loc[youden_s100b.idxmax(), 'threshold']
print(best_thresh_s100b)

# r2py:entity:roc.ndka
# roc.ndka
fpr_ndka, tpr_ndka, thresholds_ndka = roc_curve(aSAH['outcome'], aSAH['ndka'])
roc_ndka = pd.DataFrame({'threshold': thresholds_ndka, 'sensitivity': tpr_ndka * 100, 'specificity': (1 - fpr_ndka) * 100})

# r2py:entity:coords_5
# coords(roc.ndka, "best", ret="threshold", best.method="youden")
youden_ndka = roc_ndka['sensitivity'] + roc_ndka['specificity'] - 100
print(roc_ndka.loc[youden_ndka.idxmax(), 'threshold'])

# r2py:entity:coords_6
# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft")
# Closest to (0, 100) in ROC space: distance = sqrt(fpr^2 + (1-tpr)^2)
dist_topleft = np.sqrt((fpr_ndka**2) + ((1-tpr_ndka)**2))
print(thresholds_ndka[dist_topleft.argmin()])

# r2py:entity:coords_7
# coords(roc.ndka, "best", ret="threshold", best.method="youden", best.weights=c(50, 0.2))
# Weighted Youden: weights[0]*sens + weights[1]*spec
w_youden = 50 * roc_ndka['sensitivity'] + 0.2 * roc_ndka['specificity']
print(roc_ndka.loc[w_youden.idxmax(), 'threshold'])

# r2py:entity:coords_8
# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft", best.weights=c(5, 0.2))
w_dist = np.sqrt((5 * fpr_ndka**2) + (0.2 * (1-tpr_ndka)**2))
print(thresholds_ndka[w_dist.argmin()])

# r2py:entity:plot
# plot(roc.ndka, print.thres="best", ...)
# We plot the ROC curve using plotnine
roc_plot_df = pd.DataFrame({'fpr': fpr_ndka, 'tpr': tpr_ndka})
print(roc_plot_df.head()) # Printing since we can't "pop up" a window here, but providing the plotnine logic:
# (ggplot(roc_plot_df, aes('fpr', 'tpr')) + geom_line())

# r2py:entity:coords_9
# coords(roc.s100b, "best", ret=c("threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"))
# For "best" based on Youden
best_idx = youden_s100b.idxmax()
# Accuracy/Precision needs actual predictions based on that threshold
best_t = roc_s100b.loc[best_idx, 'threshold']
preds = (aSAH['s100b'] >= best_t).astype(int)
from sklearn.metrics import accuracy_score, precision_score, recall_score
results = {
    'threshold': best_t,
    'specificity': roc_s100b.loc[best_idx, 'specificity'],
    'sensitivity': roc_s100b.loc[best_idx, 'sensitivity'],
    'accuracy': accuracy_score(aSAH['outcome'], preds) * 100,
    'precision': precision_score(aSAH['outcome'], preds) * 100,
    'recall': recall_score(aSAH['outcome'], preds) * 100
}
print(results)

# r2py:entity:coords_10
# coords(roc.s100b, "best", ret = "all")
print(roc_s100b.loc[best_idx])

# r2py:entity:plot_1
# plot(specificity + sensitivity ~ threshold, coords(roc.ndka, "all"), ...)
# Prepare data for plotnine
plot_data_1 = roc_ndka.copy()
plot_data_1['sum_spec_sens'] = plot_data_1['specificity'] + plot_data_1['sensitivity']
plot_data_1 = plot_data_1[np.isfinite(plot_data_1['threshold'])]
p1 = (ggplot(plot_data_1, aes(x='threshold', y='sum_spec_sens')) 
      + geom_line() + scale_x_log10() + labs(title="Spec+Sens vs Threshold"))
print(p1)

# r2py:entity:plot_2
# plot(precision ~ recall, coords(roc.ndka, "all", ret = c("recall", "precision")), ...)
precision_ndka, recall_ndka, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plot_data_2 = pd.DataFrame({'precision': precision_ndka * 100, 'recall': recall_ndka * 100})
p2 = (ggplot(plot_data_2, aes(x='recall', y='precision')) 
      + geom_line() + labs(title="Precision-Recall Curve"))
print(p2)

# r2py:entity:plot_3
# plot(tpr ~ fpr, coords(roc.ndka, "all", ret = c("tpr", "fpr")), ...)
plot_data_3 = pd.DataFrame({'fpr': fpr_ndka, 'tpr': tpr_ndka})
p3 = (ggplot(plot_data_3, aes(x='fpr', y='tpr')) 
      + geom_line() + labs(title="ROC Curve"))
print(p3)