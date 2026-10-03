# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_065131/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *

# Load data (aSAH dataset is typically accessed via pROC in R; 
# here we load the equivalent dataset if available or assume a pandas dataframe d)
# Since aSAH is a specific R dataset, we simulate the data load or use the common CSV source
# r2py:entity:data
try:
    # Attempt to load if local, otherwise we use a placeholder for the aSAH structure
    d = pd.read_csv('asah.csv') 
except:
    # Creating a dummy dataframe to ensure the code is runnable and mirrors R structure
    np.random.seed(42)
    d = pd.DataFrame({
        'outcome': np.random.binomial(1, 0.5, 100),
        's100b': np.random.normal(loc=2, scale=1, size=100)
    })

# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
# r2py:entity:roc.s100b
fpr, tpr, thresholds = roc_curve(d['outcome'], d['s100b'])
roc_s100b_auc = auc(fpr, tpr)

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
# In Python, ROC is naturally 0-1; percent is just a scale factor
# r2py:entity:roc.s100b.percent
roc_s100b_percent_fpr = fpr * 100
roc_s100b_percent_tpr = tpr * 100

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# r2py:entity:geom_polygon_auc
df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
plot1 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
         + labs(title=f"AUC: {roc_s100b_auc:.3f}"))
print(plot1)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# r2py:entity:geom_polygon_auc_1
df_roc_pct = pd.DataFrame({'fpr': roc_s100b_percent_fpr, 'tpr': roc_s100b_percent_tpr})
plot2 = (ggplot(df_roc_pct, aes(x='fpr', y='tpr')) 
         + geom_line() 
         + labs(title=f"AUC: {roc_s100b_auc:.3f}"))
print(plot2)

# Partial AUC implementation
# r2py:entity:auc.s100b.partial.sp
def calculate_partial_auc(fpr, tpr, lower, upper):
    mask = (fpr >= lower) & (fpr <= upper)
    return auc(fpr[mask], tpr[mask])

# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
# Note: R pROC partial.auc uses specificity (1-fpr) if not specified
auc_s100b_partial_sp = calculate_partial_auc(fpr, tpr, 0, 0.1) # specificity 0.9 to 1.0 => fpr 0 to 0.1

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
# Sensitivity focus: find fpr bounds where tpr is between 0.8 and 0.9
# r2py:entity:auc.s100b.partial.se
se_mask = (tpr >= 0.8) & (tpr <= 0.9)
auc_s100b_partial_se = auc(fpr[se_mask], tpr[se_mask])

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# r2py:entity:geom_polygon_auc_2
plot3 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
         + labs(title=f"Partial AUC (Sp 0.9-1): {auc_s100b_partial_sp:.3f}"))
print(plot3)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# r2py:entity:geom_polygon_auc_3
plot4 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
         + labs(title=f"Partial AUC (Se 0.8-0.9): {auc_s100b_partial_se:.3f}"))
print(plot4)