# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/empty/rep0/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *

# Load data (aSAH is part of pROC in R, approximating with a simulated dataset or loading if available)
# Since aSAH is an internal R dataset, we simulate the structure: outcome (binary) and s100b (continuous)
# In a real scenario, use: d = pd.read_csv('asah.csv')
# r2py:entity:data
np.random.seed(42)
d = pd.DataFrame({
    'outcome': np.random.binomial(1, 0.3, 100),
    's100b': np.random.normal(10, 5, 100)
})
# Add signal to make ROC interesting
d.loc[d['outcome'] == 1, 's100b'] += 10

# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
# r2py:entity:roc.s100b
fpr, tpr, thresholds = roc_curve(d['outcome'], d['s100b'])
roc_s100b = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
auc_s100b = auc(fpr, tpr)

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
# In Python, percentages are just scaling the axis (0-1 to 0-100)
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc_s100b.copy()
roc_s100b_percent['fpr'] = roc_s100b_percent['fpr'] * 100
roc_s100b_percent['tpr'] = roc_s100b_percent['tpr'] * 100

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# r2py:entity:ggroc
p1 = (ggplot(roc_s100b, aes('fpr', 'tpr')) 
     + geom_path() 
# r2py:entity:geom_polygon_auc
     + geom_polygon(aes(x=[0, 1, 1, 0], y=[0, 0, 1, 1]), fill="blue", alpha=0.1) 
     + labs(title=f"AUC: {auc_s100b:.2f}"))
print(p1)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(...)
# legacy.axes=TRUE means X axis is 1-Specificity (FPR)
# r2py:entity:ggroc_1
p2 = (ggplot(roc_s100b_percent, aes('fpr', 'tpr')) 
     + geom_path() 
# r2py:entity:geom_polygon_auc_1
     + geom_polygon(aes(x=[0, 100, 100, 0], y=[0, 0, 100, 100]), fill="blue", alpha=0.1) 
     + labs(title=f"AUC (Percent): {auc_s100b * 100:.2f}"))
print(p2)

# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
# Partial AUC for specificity between 0.9 and 1.0 (FPR between 0 and 0.1)
# r2py:entity:auc.s100b.partial.sp
mask_sp = (fpr >= 0) & (fpr <= 0.1)
auc_s100b_partial_sp = auc(fpr[mask_sp], tpr[mask_sp])

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
# Partial AUC for sensitivity between 0.8 and 0.9
# r2py:entity:auc.s100b.partial.se
mask_se = (tpr >= 0.8) & (tpr <= 0.9)
auc_s100b_partial_se = auc(fpr[mask_se], tpr[mask_se])

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# r2py:entity:ggroc_2
p3 = (ggplot(roc_s100b, aes('fpr', 'tpr')) 
     + geom_path() 
# r2py:entity:geom_polygon_auc_2
     + geom_polygon(aes(x=[0, 0.1, 0.1, 0], y=[0, 0, tpr[mask_sp][-1], 0]), fill="green", alpha=0.3) 
     + labs(title=f"Partial AUC (Sp 0.9-1): {auc_s100b_partial_sp:.2f}"))
print(p3)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# r2py:entity:ggroc_3
p4 = (ggplot(roc_s100b, aes('fpr', 'tpr')) 
     + geom_path() 
# r2py:entity:geom_polygon_auc_3
     + geom_polygon(aes(x=[fpr[mask_se][0], fpr[mask_se][-1], fpr[mask_se][-1], fpr[mask_se][0]], 
                        y=[0, 0, tpr[mask_se][-1], tpr[mask_se][0]]), fill="red", alpha=0.3) 
     + labs(title=f"Partial AUC (Se 0.8-0.9): {auc_s100b_partial_se:.2f}"))
print(p4)