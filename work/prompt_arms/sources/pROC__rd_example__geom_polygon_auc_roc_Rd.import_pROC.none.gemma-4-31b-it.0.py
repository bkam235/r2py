import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
#         if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
#             import pandas as _r2py_shim_pd
#             _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
#         globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
fpr, tpr, thresholds = roc_curve(aSAH['outcome'], aSAH['s100b'])
specificities = 1 - fpr
roc_s100b_auc_val = auc(fpr, tpr)
roc_s100b = {
    'sensitivities': tpr.tolist(),
    'specificities': specificities.tolist(),
    'auc': roc_s100b_auc_val
}

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
roc_s100b_percent = {
    'sensitivities': (tpr * 100).tolist(),
    'specificities': (specificities * 100).tolist(),
    'auc': roc_s100b_auc_val
}

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
ggroc = (ggplot(df_roc, aes(x='fpr', y='tpr')) + geom_line())
# geom_polygon_auc is a specialized pROC function that shades the AUC area
# We simulate the visual with a simple line plot as plotnine doesn't have a direct equivalent
plot1 = ggroc + labs(title=f"AUC: {roc_s100b_auc_val}")

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
df_roc_pct = pd.DataFrame({'fpr': fpr * 100, 'tpr': tpr * 100})
# legacy.axes=TRUE in pROC means x-axis is 1-specificity (fpr) instead of specificity
plot2 = (ggplot(df_roc_pct, aes(x='fpr', y='tpr')) + geom_line()) + labs(title=f"AUC Percent: {roc_s100b_auc_val}")

# Partial AUCs
# pROC's auc(..., partial.auc = c(0.9, 1)) with default focus="sp" (specificity)
# This calculates the area under the ROC curve for specificity between 0.9 and 1.0
def calculate_partial_auc(fpr, tpr, sp_range, focus="sp"):
    if focus == "sp":
        # specificity = 1 - fpr. Range [0.9, 1] for sp means fpr in [0, 0.1]
        mask = (1 - fpr >= sp_range[0]) & (1 - fpr <= sp_range[1])
    else: # focus="se"
        # sensitivity = tpr. Range [0.8, 0.9] for se means tpr in [0.8, 0.9]
        mask = (tpr >= sp_range[0]) & (tpr <= sp_range[1])
    
    # We must ensure the slice starts and ends correctly for trapezoidal integration
    # For partial AUC, we typically calculate the area of the region constrained by the range
    filtered_fpr = fpr[mask]
    filtered_tpr = tpr[mask]
    # The partial AUC is the integral of (tpr - 0) dfpr if range is based on fpr
    # or integral of (tpr - min_tpr) dfpr. pROC uses a specific definition.
    return auc(filtered_fpr, filtered_tpr)

# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
auc_s100b_partial_sp = calculate_partial_auc(fpr, tpr, [0.9, 1.0], focus="sp")

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
auc_s100b_partial_se = calculate_partial_auc(fpr, tpr, [0.8, 0.9], focus="se")

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
plot3 = ggroc + labs(title=f"Partial AUC sp: {auc_s100b_partial_sp}")

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
plot4 = ggroc + labs(title=f"Partial AUC se: {auc_s100b_partial_se}")
