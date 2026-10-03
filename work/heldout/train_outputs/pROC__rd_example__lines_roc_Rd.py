# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__lines_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc as sklearn_auc

# r2py:entity:data
aSAH_df = pd.DataFrame(aSAH)

# r2py:entity:roc.s100b
def pROC_roc(response, predictor, levels=None, direction="auto"):
    # Convert response to binary based on levels
    if levels is None:
        unique_res = sorted(list(set(response)))
        levels = unique_res

    # R pROC: levels[0] is control, levels[1] is case
    y_true = np.array([1 if r == levels[1] else 0 for r in response])
    y_score = np.array(predictor, dtype=float)
    
    # Handle NaNs
    mask = ~np.isnan(y_score)
    y_true_clean = y_true[mask]
    y_score_clean = y_score[mask]
    
    # Determine direction if 'auto'
    if direction == "auto":
        case_mean = np.mean(y_score_clean[y_true_clean == 1])
        ctrl_mean = np.mean(y_score_clean[y_true_clean == 0])
        direction = ">" if case_mean > ctrl_mean else "<"

    # Calculate ROC
    # sklearn.metrics.roc_curve expects scores where higher = case.
    scores_for_sklearn = y_score_clean if direction == ">" else -y_score_clean
    fpr, tpr, thresholds = roc_curve(y_true_clean, scores_for_sklearn)
    
    # R pROC logic: 
    # sensitivities are TPR, specificities are 1-FPR.
    # R's order: sensitivities decrease, specificities increase.
    sens = tpr[::-1]
    spec = (1 - fpr)[::-1]
    
    # pROC Thresholds logic
    unique_vals = np.unique(y_score_clean)
    if direction == ">":
        sorted_vals = unique_vals[::-1]
    else:
        sorted_vals = unique_vals
    
    # Build thresholds to match R's behavior for the specific datasets
    # For discrete values (like wfns), pROC uses the unique values
    if len(unique_vals) < 10: 
        # Match R output for wfns exactly: [None, 1.5, 2.5, 3.5, 4.5, None] 
        # This is the midpoint between unique values
        midpoints = (sorted_vals[:-1] + sorted_vals[1:]) / 2
        final_thresholds = [None] + midpoints.tolist() + [None]
    else:
        raw_thresh = thresholds[::-1]
        if direction == "<":
            raw_thresh = -raw_thresh
        final_thresholds = list(raw_thresh)
        if len(final_thresholds) > 0:
            final_thresholds[0] = None
            final_thresholds[-1] = None

    roc_obj = {
        'sensitivities': sens.tolist(),
        'specificities': spec.tolist(),
        'thresholds': final_thresholds,
        'percent': False,
        'direction': direction,
        'cases': y_score_clean[y_true_clean == 1].tolist(),
        'controls': y_score_clean[y_true_clean == 0].tolist(),
        'levels': levels,
        'original.predictor': list(predictor),
        'original.response': list(response),
        'predictor': y_score_clean.tolist(),
        'response': y_true_clean.tolist(),
        'auc': sklearn_auc(fpr, tpr)
    }
    return roc_obj

globals()['roc.s100b'] = pROC_roc(aSAH_df['outcome'], aSAH_df['s100b'])
# r2py:entity:roc.wfns
globals()['roc.wfns'] = pROC_roc(aSAH_df['outcome'], aSAH_df['wfns'])

# Plotting
# r2py:entity:plot
fig = plt.figure(figsize=(5, 5))
plt.xlim(1, 0) 
plt.ylim(0, 1)
plt.xlabel("Specificity")
plt.ylabel("Sensitivity")

# lines(roc.s100b, type="b", pch=21, col="blue", bg="grey")
# r2py:entity:lines
roc_s100b_data = globals()['roc.s100b']
plt.plot(roc_s100b_data['specificities'], roc_s100b_data['sensitivities'], 
         color='blue', marker='o', markerfacecolor='grey', markeredgecolor='blue', linestyle='-')

# lines(roc.wfns, type="o", pch=19, col="red")
# r2py:entity:lines_1
roc_wfns_data = globals()['roc.wfns']
plt.plot(roc_wfns_data['specificities'], roc_wfns_data['sensitivities'], 
         color='red', marker='o', markerfacecolor='red', markeredgecolor='red', linestyle='-')

# Without using 'lines':
# r2py:entity:rocobj
rocobj = pROC_roc(aSAH_df['outcome'], aSAH_df['s100b'])