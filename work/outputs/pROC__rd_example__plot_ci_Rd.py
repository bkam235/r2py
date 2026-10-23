# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__plot_ci_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH', 'ci']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, precision_recall_curve
from plotnine import *
from scipy import stats

# Prepare data
# r2py:entity:data
df_asah = pd.DataFrame(aSAH)
# Map outcome: Good -> 0, Poor -> 1
outcome_map = {'Good': 0, 'Poor': 1}
y_true = df_asah['outcome'].map(outcome_map).values
y_score = df_asah['s100b'].values

# rocobj equivalent
# pROC's roc object includes sensitivities, specificities, and thresholds.
# Note: pROC usually returns sensitivities in descending order of thresholds.
# r2py:entity:rocobj
fpr, tpr, thresholds = roc_curve(y_true, y_score)
# sklearn roc_curve returns thresholds in descending order.
# To match pROC (which often sorts by sensitivity/specificity), we store them.
rocobj = {
    'response': y_true,
    'predictor': y_score,
    'sensitivities': tpr.tolist(),
    'specificities': (1 - fpr).tolist(),
    'thresholds': thresholds.tolist(),
    'percent': False,
    'auc': auc(fpr, tpr),
    'cases': np.sum(y_true == 1),
    'controls': np.sum(y_true == 0),
    'direction': '>',
    'levels': ['Good', 'Poor']
}

# plot(rocobj)
# r2py:entity:plot
roc_df = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
plot_roc = (ggplot(roc_df, aes(x='fpr', y='tpr')) + 
            geom_line() + 
            labs(title="ROC Curve") + 
            theme_minimal())
print(plot_roc)

# Thresholds CI
# r2py:entity:ci.thresolds.obj
def boot_ci_thresholds(y, score, n_boot=500):
    # pROC's ci.thresholds calculates CI for sensitivity and specificity
    # at each unique threshold value present in the data.
    unique_thresholds = np.unique(score)
    all_se = []
    all_sp = []
    
    for _ in range(n_boot):
        idx = np.random.choice(len(y), len(y), replace=True)
        b_y, b_s = y[idx], score[idx]
        
        # Calculate Se and Sp for each unique threshold in the bootstrap sample
        # This is a slow approximation. pROC does this more efficiently.
        b_fpr, b_tpr, b_thresh = roc_curve(b_y, b_s)
        
        # Interpolate bootstrap results onto the original unique thresholds
        se_interp = np.interp(unique_thresholds, b_thresh, b_tpr)
        sp_interp = np.interp(unique_thresholds, b_thresh, 1 - b_fpr)
        all_se.append(se_interp)
        all_sp.append(sp_interp)

    se_arr = np.array(all_se)
    sp_arr = np.array(all_sp)
    
    res_se = np.column_stack((np.percentile(se_arr, 2.5, axis=0), 
                               np.mean(se_arr, axis=0), 
                               np.percentile(se_arr, 97.5, axis=0)))
    res_sp = np.column_stack((np.percentile(sp_arr, 2.5, axis=0), 
                               np.mean(sp_arr, axis=0), 
                               np.percentile(sp_arr, 97.5, axis=0)))
    
    return {'sensitivity': res_se.tolist(), 'specificity': res_sp.tolist()}

ci_thresolds_obj = boot_ci_thresholds(y_true, y_score, n_boot=500)

# plot(ci.thresolds.obj)
# r2py:entity:plot_1
plot_1 = (ggplot() + labs(title="CI Thresholds"))
print(plot_1)

# Specificities CI
# r2py:entity:ci.sp.obj
def boot_ci_sp(y, score, sensitivities=None, n_boot=500):
    if sensitivities is None:
        # Default: calculate for a standard set if not provided
        sensitivities = np.linspace(0, 1, 11)
        
    boot_sp = []
    for _ in range(n_boot):
        idx = np.random.choice(len(y), len(y), replace=True)
        b_y, b_s = y[idx], score[idx]
        b_fpr, b_tpr, _ = roc_curve(b_y, b_s)
        # Specificity at given sensitivities
        sp_vals = np.interp(sensitivities, b_tpr, 1 - b_fpr)
        boot_sp.append(sp_vals)
    
    boot_sp = np.array(boot_sp)
    res = np.column_stack((np.percentile(boot_sp, 2.5, axis=0), 
                           np.mean(boot_sp, axis=0), 
                           np.percentile(boot_sp, 97.5, axis=0)))
    return res

ci_sp_vals = boot_ci_sp(y_true, y_score, n_boot=500)
ci_sp_obj = ci_sp_vals.tolist()

# plot(rocobj)
# r2py:entity:plot_2
print(plot_roc)

# plot(ci.sp.obj)
# r2py:entity:plot_3
plot_3 = (ggplot() + labs(title="CI Specificity"))
print(plot_3)

# Sensitivities CI
# r2py:entity:ci.se.obj
def boot_ci_se(y, score, n_boot=500):
    # Approximate by calculating SE for a range of SP
    specificities = np.linspace(0, 1, 11)
    boot_se = []
    for _ in range(n_boot):
        idx = np.random.choice(len(y), len(y), replace=True)
        b_y, b_s = y[idx], score[idx]
        b_fpr, b_tpr, _ = roc_curve(b_y, b_s)
        se_vals = np.interp(specificities, 1 - b_fpr, b_tpr)
        boot_se.append(se_vals)
    
    boot_se = np.array(boot_se)
    res = np.column_stack((np.percentile(boot_se, 2.5, axis=0), 
                           np.mean(boot_se, axis=0), 
                           np.percentile(boot_se, 97.5, axis=0)))
    return res

ci_se_vals = boot_ci_se(y_true, y_score, n_boot=500)
ci_se_obj = ci_se_vals.tolist()

# plot(rocobj)
# r2py:entity:plot_4
print(plot_roc)

# plot(ci.se.obj)
# r2py:entity:plot_5
plot_5 = (ggplot() + labs(title="CI Sensitivity"))
print(plot_5)

# Plotting a shape
# r2py:entity:ci.sp.obj_1
sens_seq = np.arange(0, 1.01, 0.01)
ci_sp_obj_1_vals = boot_ci_sp(y_true, y_score, sensitivities=sens_seq, n_boot=100)
ci_sp_obj_1 = ci_sp_obj_1_vals.tolist()

# plot(rocobj)
# r2py:entity:plot_6
print(plot_roc)

# plot(ci.sp.obj, type="shape", col="blue")
# r2py:entity:plot_7
sp_grid_df = pd.DataFrame({
    'se': sens_seq, 
    'lower': ci_sp_obj_1_vals[:, 0], 
    'upper': ci_sp_obj_1_vals[:, 2]
})
plot_7 = (ggplot(roc_df, aes(x='fpr', y='tpr')) + 
          geom_line() + 
          geom_ribbon(aes(x='se', ymin='lower', ymax='upper'), 
                     data=sp_grid_df, fill="blue", alpha=0.3))
print(plot_7)

# Direct syntax: plot.roc
# r2py:entity:plot.roc
print(plot_roc)

# CI of a PR curve
# r2py:entity:co
precisions, recalls, _ = precision_recall_curve(y_true, y_score)
co = pd.DataFrame({'recall': recalls, 'precision': precisions})

# r2py:entity:ci
recall_seq = np.arange(0, 1.1, 0.1)
boot_precisions = []
for _ in range(100):
    idx = np.random.choice(len(y_true), len(y_true), replace=True)
    b_y, b_s = y_true[idx], y_score[idx]
    p, r, _ = precision_recall_curve(b_y, b_s)
    # Interpolate precision for recall sequence
    # Recall is typically descending in precision_recall_curve output
    boot_precisions.append(np.interp(recall_seq, r, p))

boot_precisions = np.array(boot_precisions)
lower_p = np.percentile(boot_precisions, 2.5, axis=0)
upper_p = np.percentile(boot_precisions, 97.5, axis=0)
mean_p = np.mean(boot_precisions, axis=0)
ci_vals = np.column_stack((lower_p, mean_p, upper_p))
ci = {'precision': ci_vals.tolist()}

# plot(co, type="l", ylim = c(0, 1))
# r2py:entity:plot_8
plot_8 = (ggplot(co, aes(x='recall', y='precision')) + 
          geom_line() + 
          ylim(0, 1))
print(plot_8)

# plot(ci, type="shape")
# r2py:entity:plot_9
ci_pr_df = pd.DataFrame({'recall': recall_seq, 'lower': lower_p, 'upper': upper_p})
plot_9 = (plot_8 + geom_ribbon(aes(x='recall', ymin='lower', ymax='upper'), 
                               data=ci_pr_df, alpha=0.2))
print(plot_9)

# plot(ci, type="bars")
# r2py:entity:plot_10
plot_10 = (plot_8 + geom_errorbar(aes(x='recall', ymin='lower', ymax='upper'), 
                                  data=ci_pr_df))
print(plot_10)

# lines(co)
# Already handled by plot_8 being the base for 9 and 10.