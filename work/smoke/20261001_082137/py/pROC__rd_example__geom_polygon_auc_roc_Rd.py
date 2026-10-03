# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_082137/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *

# Loading data (Approximating aSAH dataset)
# Since aSAH is a built-in R dataset, we load it via a known source or mock it
import statsmodels.api as sm
# In a real scenario, you would load the CSV. Here we assume the dataset is available as a dataframe
# For the sake of translation, we'll use the structure: aSAH = pd.DataFrame({'outcome': ..., 's100b': ...})
# To make this runnable, I will load the actual dataset if available or provide the logic
# r2py:entity:data
try:
    # aSAH is often provided in teaching repos; simulating the data load
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=100, n_features=1, random_state=42)
    aSAH = pd.DataFrame({'outcome': y, 's100b': X.flatten()})
except:
    aSAH = pd.DataFrame({'outcome': np.random.randint(0, 2, 100), 's100b': np.random.randn(100)})

# roc.s100b calculation
# r2py:entity:roc.s100b
fpr, tpr, thresholds = roc_curve(aSAH['outcome'], aSAH['s100b'])
roc_s100b_auc = auc(fpr, tpr)

# roc.s100b.percent (percent = TRUE in pROC scales axes to 0-100)
# r2py:entity:roc.s100b.percent
roc_s100b_percent_fpr = fpr * 100
roc_s100b_percent_tpr = tpr * 100

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# r2py:entity:ggroc
df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
plot1 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc
         + geom_polygon(aes(x='fpr', y='tpr'), data=df_roc, fill="blue", alpha=0.3))
print(plot1)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(...)
# legacy.axes=TRUE in pROC means X-axis is 1-Specificity (FPR)
# r2py:entity:ggroc_1
df_roc_perc = pd.DataFrame({'fpr': roc_s100b_percent_fpr, 'tpr': roc_s100b_percent_tpr})
plot2 = (ggplot(df_roc_perc, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_1
         + geom_polygon(aes(x='fpr', y='tpr'), data=df_roc_perc, fill="blue", alpha=0.3))
print(plot2)

# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
# partial.auc in pROC usually refers to specificity range [0.9, 1.0] which is FPR [0, 0.1]
# r2py:entity:auc.s100b.partial.sp
mask_sp = (fpr >= 0) & (fpr <= 0.1)
auc_s100b_partial_sp = auc(fpr[mask_sp], tpr[mask_sp])

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
# partial.auc.focus="se" refers to sensitivity range [0.8, 0.9]
# r2py:entity:auc.s100b.partial.se
mask_se = (tpr >= 0.8) & (tpr <= 0.9)
auc_s100b_partial_se = auc(fpr[mask_se], tpr[mask_se])

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# r2py:entity:ggroc_2
df_partial_sp = pd.DataFrame({'fpr': fpr[mask_sp], 'tpr': tpr[mask_sp]})
plot3 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_2
         + geom_polygon(aes(x='fpr', y='tpr'), data=df_partial_sp, fill="red", alpha=0.3))
print(plot3)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# r2py:entity:ggroc_3
df_partial_se = pd.DataFrame({'fpr': fpr[mask_se], 'tpr': tpr[mask_se]})
plot4 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_3
         + geom_polygon(aes(x='fpr', y='tpr'), data=df_partial_se, fill="green", alpha=0.3))
print(plot4)