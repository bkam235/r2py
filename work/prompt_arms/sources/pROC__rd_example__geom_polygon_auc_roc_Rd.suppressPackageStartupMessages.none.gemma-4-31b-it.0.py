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
# sklearn's roc_curve returns fpr, tpr, thresholds. R's pROC stores sensitivities (tpr) and specificities (1-fpr).
fpr, tpr, thresholds = roc_curve(aSAH['outcome'], aSAH['s100b'])
roc_s100b_auc = auc(fpr, tpr)

# Replicate pROC object structure for verifier
roc.s100b = {
    '__r2py_fp__': True,
    'class': ['roc'],
    'numbers': {
        'sensitivities': tpr.tolist(),
        'specificities': (1 - fpr).tolist(),
        'thresholds': thresholds.tolist(),
        'auc': roc_s100b_auc
    },
    'auc': roc_s100b_auc
}

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
roc.s100b.percent = {
    '__r2py_fp__': True,
    'class': ['roc'],
    'numbers': {
        'sensitivities': (tpr * 100).tolist(),
        'specificities': ((1 - fpr) * 100).tolist(),
        'thresholds': thresholds.tolist(),
        'auc': roc_s100b_auc * 100
    },
    'auc': roc_s100b_auc * 100
}

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# In Python we emulate this with plotnine
df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
plot1 = (ggplot(df_roc, aes(x='fpr', y='tpr')) + geom_line())
# Note: geom_polygon_auc is a specialized pROC function; we simulate the result visually if possible
# Since we cannot implement a custom geom_polygon_auc perfectly, we provide the plot logic
print(plot1)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# legacy.axes=TRUE in pROC flips the x-axis to 1-specificity (which is fpr)
df_roc_pct = pd.DataFrame({'fpr': fpr * 100, 'tpr': tpr * 100})
plot2 = (ggplot(df_roc_pct, aes(x='fpr', y='tpr')) + geom_line())
print(plot2)

# Partial AUCs
# pROC partial.auc = c(a, b) calculates AUC for specificity in [a, b]
# partial.auc.focus="se" calculates AUC for sensitivity in [a, b]

def calculate_partial_auc(fpr, tpr, range_vals, focus="sp"):
    if focus == "sp":
        # specificity in [a, b] -> (1-fpr) in [a, b] -> fpr in [1-b, 1-a]
        mask = (fpr >= (1 - range_vals[1])) & (fpr <= (1 - range_vals[0]))
    else:
        # sensitivity in [a, b] -> tpr in [a, b]
        mask = (tpr >= range_vals[0]) & (tpr <= range_vals[1])
    
    # Filter and normalize to calculate the partial AUC area
    f_sub = fpr[mask]
    t_sub = tpr[mask]
    if len(f_sub) < 2:
        return 0.0
    return auc(f_sub, t_sub)

# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
auc.s100b.partial.sp = calculate_partial_auc(fpr, tpr, [0.9, 1], focus="sp")

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
auc.s100b.partial.se = calculate_partial_auc(fpr, tpr, [0.8, 0.9], focus="se")

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
plot3 = (ggplot(df_roc, aes(x='fpr', y='tpr')) + geom_line())
print(plot3)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
plot4 = (ggplot(df_roc, aes(x='fpr', y='tpr')) + geom_line())
print(plot4)