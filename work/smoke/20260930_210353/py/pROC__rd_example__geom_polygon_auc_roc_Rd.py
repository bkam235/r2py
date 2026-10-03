# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_210353/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *

# Loading the aSAH dataset
# Since aSAH is a built-in R dataset, we simulate the data structure 
# or assume it is loaded as a pandas DataFrame.
# In a real scenario, you would load the CSV: d = pd.read_csv('aSAH.csv')
# r2py:entity:data
from sklearn.datasets import make_classification
# Mocking aSAH data for functionality since it's an R-specific dataset
# Outcome (binary), s100b (continuous)
np.random.seed(42)
d = pd.DataFrame({
    'outcome': np.random.randint(0, 2, 100),
    's100b': np.random.randn(100)
})

# roc.s100b
# r2py:entity:roc.s100b
fpr, tpr, thresholds = roc_curve(d['outcome'], d['s100b'])
roc_s100b_auc = auc(fpr, tpr)
roc_s100b = pd.DataFrame({'fpr': fpr, 'tpr': tpr})

# roc.s100b.percent
# In R's pROC, percent=TRUE scales axes to 0-100
# r2py:entity:roc.s100b.percent
roc_s100b_percent = roc_s100b.copy()
roc_s100b_percent['fpr'] = roc_s100b_percent['fpr'] * 100
roc_s100b_percent['tpr'] = roc_s100b_percent['tpr'] * 100

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# r2py:entity:ggroc
plot1 = (ggplot(roc_s100b, aes('fpr', 'tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc
         + geom_polygon(aes('fpr', 'tpr'), data=pd.DataFrame({'fpr': [0, 1, 1, 0], 'tpr': [0, 0, 1, 1]}), fill="grey", alpha=0.3)
         + labs(title=f"AUC: {roc_s100b_auc:.4f}"))

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(...)
# r2py:entity:ggroc_1
plot2 = (ggplot(roc_s100b_percent, aes('fpr', 'tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_1
         + geom_polygon(aes('fpr', 'tpr'), data=pd.DataFrame({'fpr': [0, 100, 100, 0], 'tpr': [0, 0, 100, 0]}), fill="grey", alpha=0.3)
         + labs(title=f"AUC: {roc_s100b_auc:.4f}"))

# partial AUC functions approximation
# r2py:entity:auc.s100b.partial.sp
def calculate_partial_auc(fpr, tpr, specificity_range):
    # specificity = 1 - fpr
    # range [0.9, 1] specificity means fpr range [0, 0.1]
    mask = (1 - fpr >= specificity_range[0]) & (1 - fpr <= specificity_range[1])
    return auc(fpr[mask], tpr[mask])

# auc.s100b.partial.sp (Specificity 0.9 to 1)
auc_s100b_partial_sp = calculate_partial_auc(fpr, tpr, [0.9, 1.0])

# r2py:entity:auc.s100b.partial.se
# auc.s100b.partial.se (Sensitivity/Specificity range 0.8 to 0.9)
auc_s100b_partial_se = calculate_partial_auc(fpr, tpr, [0.8, 0.9])

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# Note: geom_polygon_auc for partial AUC highlights the specific region under the curve
# r2py:entity:ggroc_2
plot3 = (ggplot(roc_s100b, aes('fpr', 'tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_2
         + geom_polygon(aes('fpr', 'tpr'), data=pd.DataFrame({'fpr': [0, 0.1, 0.1, 0], 'tpr': [0, 0, 1, 0]}), fill="blue", alpha=0.3)
         + labs(title=f"Partial AUC (Spec 0.9-1): {auc_s100b_partial_sp:.4f}"))

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# r2py:entity:ggroc_3
plot4 = (ggplot(roc_s100b, aes('fpr', 'tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_3
         + geom_polygon(aes('fpr', 'tpr'), data=pd.DataFrame({'fpr': [0.1, 0.2, 0.2, 0.1], 'tpr': [0, 0, 1, 0]}), fill="green", alpha=0.3)
         + labs(title=f"Partial AUC (Spec 0.8-0.9): {auc_s100b_partial_se:.4f}"))

# Display plots (if in notebook)
print(plot1)
print(plot2)
print(plot3)
print(plot4)