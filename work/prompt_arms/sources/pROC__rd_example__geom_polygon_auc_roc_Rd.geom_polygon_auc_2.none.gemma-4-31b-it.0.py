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

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *

# Helper to mimic pROC roc object structure
def create_roc_object(y_true, y_score, percent=False):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    # pROC's sensitivities are tpr, specificities are 1-fpr
    sens = tpr
    spec = 1 - fpr
    if percent:
        sens = sens * 100
        spec = spec * 100
    
    # Calculate total AUC
    total_auc = auc(fpr, tpr)
    
    return {
        '__r2py_fp__': True,
        'class': ['roc'],
        'numbers': {
            'sensitivities': sens.tolist(),
            'specificities': spec.tolist(),
            'auc': total_auc
        },
        'auc': total_auc
    }

# Create ROC curves
roc_s100b = create_roc_object(aSAH['outcome'], aSAH['s100b'])
roc_s100b_percent = create_roc_object(aSAH['outcome'], aSAH['s100b'], percent=True)

# Plotting (ggroc + geom_polygon_auc)
# Note: In a real scenario, geom_polygon_auc fills the area under the curve.
# We simulate this with plotnine.

# 1. ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
df_roc = pd.DataFrame({'fpr': 1 - np.array(roc_s100b['numbers']['specificities']), 'tpr': np.array(roc_s100b['numbers']['sensitivities'])})
plot_1 = ggplot(df_roc, aes(x='fpr', y='tpr')) + geom_path() + geom_polygon(aes(x='fpr', y='tpr'), fill="grey", alpha=0.3)

# 2. ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# legacy.axes=TRUE in pROC means x-axis is 1-specificity (FPR) but plotted from 1 to 0
df_roc_pct = pd.DataFrame({'fpr': 100 * (1 - np.array(roc_s100b_percent['numbers']['specificities'])), 'tpr': np.array(roc_s100b_percent['numbers']['sensitivities'])})
plot_2 = ggplot(df_roc_pct, aes(x='fpr', y='tpr')) + geom_path() + geom_polygon(aes(x='fpr', y='tpr'), fill="grey", alpha=0.3)

# Partial AUCs
# pROC partial.auc is defined over a range of specificity (usually)
# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
# Focus is specificity by default
def calculate_pauc(roc_obj, pauc_range, focus="sp"):
    fpr = 1 - np.array(roc_obj['numbers']['specificities'])
    tpr = np.array(roc_obj['numbers']['sensitivities'])
    
    if focus == "sp":
        # Range is based on specificity
        spec = np.array(roc_obj['numbers']['specificities'])
        mask = (spec >= pauc_range[0]) & (spec <= pauc_range[1])
    else:
        # Focus on sensitivity
        sens = np.array(roc_obj['numbers']['sensitivities'])
        mask = (sens >= pauc_range[0]) & (sens <= pauc_range[1])
        
    return auc(fpr[mask], tpr[mask])

auc_s100b_partial_sp = calculate_pauc(roc_s100b, [0.9, 1])
auc_s100b_partial_se = calculate_pauc(roc_s100b, [0.8, 0.9], focus="se")

# 3 & 4. Plots with Partial AUC
plot_3 = ggplot(df_roc, aes(x='fpr', y='tpr')) + geom_path()
plot_4 = ggplot(df_roc, aes(x='fpr', y='tpr')) + geom_path()