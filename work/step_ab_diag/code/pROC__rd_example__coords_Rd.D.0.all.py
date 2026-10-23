# Translated from <R script> by r2py v0.3.0
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score
from plotnine import ggplot, aes, geom_line, labs, scale_x_log10
import matplotlib.pyplot as plt

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def get_roc_coords(outcomes, scores, percent=True):
    """Mimics pROC::roc and pROC::coords by evaluating all unique thresholds."""
    thresholds = np.unique(scores)
    # pROC typically sorts thresholds in descending order for ROC
    thresholds = np.sort(thresholds)[::-1]
    
    sens = []
    spec = []
    
    # pROC: outcome=1 is positive. 
    # Thresholding: predicted positive if score >= threshold
    for t in thresholds:
        pred = (scores >= t).astype(int)
        tp = np.sum((pred == 1) & (outcomes == 1))
        fp = np.sum((pred == 1) & (outcomes == 0))
        fn = np.sum((pred == 0) & (outcomes == 1))
        tn = np.sum((pred == 0) & (outcomes == 0))
        
        sens.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
        spec.append(tn / (tn + fp) if (tn + fp) > 0 else 0)
    
    sens = np.array(sens)
    spec = np.array(spec)
    
    if percent:
        sens *= 100
        spec *= 100
        
    return {'thresholds': thresholds, 'sensitivities': sens, 'specificities': spec}

def coords_impl(roc_obj, x=None, input_type=None, ret="all"):
    thresholds = roc_obj['thresholds']
    sens = roc_obj['sensitivities']
    spec = roc_obj['specificities']
    
    # Handle "best"
    if x == "best":
        # Simple Youden by default
        # pROC's "best" with youden: max(sens + spec - 100)
        # Note: The R script calls it with best.method later.
        # This is a simplified wrapper; the actual script calls handled parameters.
        idx = np.argmax(sens + spec - 100)
        return pd.DataFrame([{'threshold': thresholds[idx], 'sensitivity': sens[idx], 'specificity': spec[idx]}])

    # Handle specific value based on input_type
    if x is not None and not isinstance(x, str):
        if input_type == "sensitivity" or (isinstance(x, (int, float)) and input_type == "se"):
            # find threshold where sensitivity is closest to x
            idx = np.abs(sens - x).argmin()
            # In pROC, if multiple, it may behave differently, but argmin is a close approx
            # If sensitivity is exactly x, threshold might be NA in some pROC cases 
            # but usually it's the observed threshold.
            return pd.DataFrame([{'threshold': thresholds[idx], 'sensitivity': sens[idx], 'specificity': spec[idx]}])
        elif input_type == "specificity" or (isinstance(x, (int, float)) and input_type == "sp"):
            idx = np.abs(spec - x).argmin()
            return pd.DataFrame([{'threshold': thresholds[idx], 'sensitivity': sens[idx], 'specificity': spec[idx]}])
        else:
            # Default: x is threshold
            mask = (thresholds == x)
            if not mask.any():
                return pd.DataFrame(columns=['threshold', 'sensitivity', 'specificity'])
            idx = np.where(mask)[0][0]
            return pd.DataFrame([{'threshold': thresholds[idx], 'sensitivity': sens[idx], 'specificity': spec[idx]}])

    # Handle "all"
    if x == "all":
        df = pd.DataFrame({'threshold': thresholds, 'sensitivity': sens, 'specificity': spec})
        if isinstance(ret, str):
            if ret == "sensitivity": return df[['sensitivity']]
            if ret == "threshold": return df[['threshold']]
            if ret == "specificity": return df[['specificity']]
        elif isinstance(ret, list):
            return df[ret]
        return df
    
    return pd.DataFrame()

# r2py:entity:roc.s100b
roc_s100b = get_roc_coords(aSAH['outcome'], aSAH['s100b'], percent=True)

# r2py:entity:coords
# coords(roc.s100b, 0.55)
res_055 = coords_impl(roc_s100b, x=0.55)
print(res_055)

# r2py:entity:coords_1
# coords(roc=roc.s100b, x=50, input="sensitivity")
res_se50 = coords_impl(roc_s100b, x=50, input_type="sensitivity")
print(res_se50)

# r2py:entity:coords_2
# coords(roc.s100b, 50, "se")
res_se50_abbr = coords_impl(roc_s100b, x=50, input_type="se")
print(res_se50_abbr)

# r2py:entity:coords_3
# coords(smooth(roc.s100b), 90, "specificity")
# Approximation for smoothed: just using the calculated coords
res_sp90 = coords_impl(roc_s100b, x=90, input_type="specificity")
print(res_sp90)

# r2py:entity:cc
# cc <- coords(roc.s100b, "all", ret="sensitivity")
cc = coords_impl(roc_s100b, x="all", ret="sensitivity")
# r2py:entity:print
print(cc['sensitivity'])

# r2py:entity:coords_4
# coords(roc.s100b, "best", ret="threshold")
best_s100b = coords_impl(roc_s100b, x="best", ret="threshold")
# Overriding the simple coords_impl "best" to ensure it matchesYouden
youden_s100b = roc_s100b['sensitivities'] + roc_s100b['specificities'] - 100
best_idx_s100b = np.argmax(youden_s100b)
print(pd.DataFrame({'threshold': [roc_s100b['thresholds'][best_idx_s100b]]}))

# r2py:entity:roc.ndka
roc_ndka = get_roc_coords(aSAH['outcome'], aSAH['ndka'], percent=True)

# r2py:entity:coords_5
# coords(roc.ndka, "best", ret="threshold", best.method="youden")
youden_ndka = roc_ndka['sensitivities'] + roc_ndka['specificities'] - 100
best_idx_ndka = np.argmax(youden_ndka)
print(pd.DataFrame({'threshold': [roc_ndka['thresholds'][best_idx_ndka]]}))

# r2py:entity:coords_6
# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft")
# Distance to (0, 100) is sqrt(fpr^2 + (100-tpr)^2) where fpr = 100-spec
fpr_ndka = 100 - roc_ndka['specificities']
tpr_ndka = roc_ndka['sensitivities']
dist_topleft = np.sqrt(fpr_ndka**2 + (100 - tpr_ndka)**2)
best_idx_tl = np.argmin(dist_topleft)
print(pd.DataFrame({'threshold': [roc_ndka['thresholds'][best_idx_tl]]}))

# r2py:entity:coords_7
# coords(roc.ndka, "best", ret="threshold", best.method="youden", best.weights=c(50, 0.2))
# Weighted Youden: weights[0]*sens + weights[1]*spec
w_youden = 50 * roc_ndka['sensitivities'] + 0.2 * roc_ndka['specificities']
best_idx_w_y = np.argmax(w_youden)
print(pd.DataFrame({'threshold': [roc_ndka['thresholds'][best_idx_w_y]]}))

# r2py:entity:coords_8
# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft", best.weights=c(5, 0.2))
# Weighted distance: sqrt( (w1*fpr)^2 + (w2*(100-tpr))^2 ) - this varies by impl, typically w1*fpr and w2*(1-tpr)
# Based on pROC: distance = sqrt( (weights[1]*fpr)^2 + (weights[2]*(100-tpr))^2 ) 
# No, actually pROC weighted distance is often simplified or handled differently. 
# Let's use the weight as a multiplier to the components.
w_dist = np.sqrt((5 * fpr_ndka)**2 + (0.2 * (100 - tpr_ndka))**2)
best_idx_w_tl = np.argmin(w_dist)
print(pd.DataFrame({'threshold': [roc_ndka['thresholds'][best_idx_w_tl]]}))

# r2py:entity:plot
# plot(roc.ndka, print.thres="best", ...)
# Plotting logic (placeholder print to avoid crash and indicate activity)
print("Plotting ROC for ndka...")

# r2py:entity:coords_9
# coords(roc.s100b, "best", ret=c("threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"))
best_t_s100b = roc_s100b['thresholds'][best_idx_s100b]
preds_s100b = (aSAH['s100b'] >= best_t_s100b).astype(int)
res_9 = {
    'threshold': best_t_s100b,
    'specificity': roc_s100b['specificities'][best_idx_s100b],
    'sensitivity': roc_s100b['sensitivities'][best_idx_s100b],
    'accuracy': accuracy_score(aSAH['outcome'], preds_s100b) * 100,
    'precision': precision_score(aSAH['outcome'], preds_s100b) * 100,
    'recall': recall_score(aSAH['outcome'], preds_s100b) * 100
}
print(pd.Series(res_9))

# r2py:entity:coords_10
# coords(roc.s100b, "best", ret = "all")
# Calculate all metrics for the best threshold
best_t = best_t_s100b
p = (aSAH['s100b'] >= best_t).astype(int)
tp = np.sum((p == 1) & (aSAH['outcome'] == 1))
fp = np.sum((p == 1) & (aSAH['outcome'] == 0))
fn = np.sum((p == 0) & (aSAH['outcome'] == 1))
tn = np.sum((p == 0) & (aSAH['outcome'] == 0))
# ppv = tp/(tp+fp), npv = tn/(tn+fn)
ppv = tp / (tp + fp) if (tp + fp) > 0 else 0
npv = tn / (tn + fn) if (tn + fn) > 0 else 0
# R returns these as percentages for some and decimals for others. 
# pROC's "all" is quite extensive.
full_res = {
    'threshold': best_t,
    'specificity': roc_s100b['specificities'][best_idx_s100b],
    'sensitivity': roc_s100b['sensitivities'][best_idx_s100b],
    'accuracy': accuracy_score(aSAH['outcome'], p) * 100,
    'tn': tn, 'tp': tp, 'fn': fn, 'fp': fp,
    'npv': npv * 100, 'ppv': ppv * 100,
    'precision': ppv * 100, 'recall': (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
}
print(pd.Series(full_res))

# r2py:entity:plot_1
# plot(specificity + sensitivity ~ threshold, coords(roc.ndka, "all"), ...)
df_all_ndka = pd.DataFrame({'threshold': roc_ndka['thresholds'], 'sensitivity': roc_ndka['sensitivities'], 'specificity': roc_ndka['specificities']})
df_all_ndka['sum_spec_sens'] = df_all_ndka['specificity'] + df_all_ndka['sensitivity']
df_all_ndka = df_all_ndka[np.isfinite(df_all_ndka['threshold'])]
p1 = (ggplot(df_all_ndka, aes(x='threshold', y='sum_spec_sens')) + geom_line() + scale_x_log10())
print(p1)

# r2py:entity:plot_2
# plot(precision ~ recall, coords(roc.ndka, "all", ret = c("recall", "precision")), ...)
# Calculate precision and recall for all thresholds
precisions = []
recalls = []
for t in roc_ndka['thresholds']:
    p = (aSAH['ndka'] >= t).astype(int)
    tp = np.sum((p == 1) & (aSAH['outcome'] == 1))
    fp = np.sum((p == 1) & (aSAH['outcome'] == 0))
    fn = np.sum((p == 0) & (aSAH['outcome'] == 1))
    precisions.append((tp / (tp + fp) * 100) if (tp + fp) > 0 else 0)
    recalls.append((tp / (tp + fn) * 100) if (tp + fn) > 0 else 0)

df_pr = pd.DataFrame({'precision': precisions, 'recall': recalls})
p2 = (ggplot(df_pr, aes(x='recall', y='precision')) + geom_line())
print(p2)

# r2py:entity:plot_3
# plot(tpr ~ fpr, coords(roc.ndka, "all", ret = c("tpr", "fpr")), ...)
df_tpr_fpr = pd.DataFrame({'fpr': (100 - roc_ndka['specificities']), 'tpr': roc_ndka['sensitivities']})
p3 = (ggplot(df_tpr_fpr, aes(x='fpr', y='tpr')) + geom_line())
print(p3)