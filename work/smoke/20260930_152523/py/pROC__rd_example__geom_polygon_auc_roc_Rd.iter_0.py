# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_152523/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *
from pyroc import ROC # Using pyroc or sklearn approximation for AUC calculations

# r2py:entity:data
# Loading data (Approximating data(aSAH) since it is a package dataset)
# In a real scenario, you would load the CSV/Dataset containing outcome and s100b
import statsmodels.api as sm
# Since aSAH is from pROC, we simulate the structure or assume a dataframe 'aSAH' exists
# For the sake of the translation, we assume aSAH is a pandas DataFrame
# aSAH = pd.read_csv("asah.csv") 

# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
# r2py:entity:roc.s100b
fpr, tpr, thresholds = roc_curve(aSAH['outcome'], aSAH['s100b'])
roc_s100b_auc = auc(fpr, tpr)

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
# Percent scale is simply scaling axes by 100
# r2py:entity:roc.s100b.percent
fpr_p = fpr * 100
tpr_p = tpr * 100

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
# r2py:entity:ggroc
df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
plot1 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc
         + geom_polygon(aes(x='fpr', y='tpr'), fill="blue", alpha=0.3))
print(plot1)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# r2py:entity:ggroc_1
df_roc_p = pd.DataFrame({'fpr': fpr_p, 'tpr': tpr_p})
plot2 = (ggplot(df_roc_p, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_1
         + geom_polygon(aes(x='fpr', y='tpr'), fill="blue", alpha=0.3))
print(plot2)

# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
# Partial AUC calculation (Trapezoidal rule for specific FPR range)
# r2py:entity:auc.s100b.partial.sp
def calculate_partial_auc(fpr, tpr, lower, upper):
    mask = (fpr >= lower) & (fpr <= upper)
    return auc(fpr[mask], tpr[mask])

auc_s100b_partial_sp = calculate_partial_auc(fpr, tpr, 0.9, 1.0)

# r2py:entity:auc.s100b.partial.se
# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
auc_s100b_partial_se = calculate_partial_auc(fpr, tpr, 0.8, 0.9)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# Filter coordinates for the polygon areas
# r2py:entity:ggroc_2
df_sp = df_roc[(df_roc['fpr'] >= 0.9) & (df_roc['fpr'] <= 1.0)]
plot3 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_2
         + geom_polygon(data=df_sp, aes(x='fpr', y='tpr'), fill="green", alpha=0.3))
print(plot3)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# r2py:entity:ggroc_3
df_se = df_roc[(df_roc['fpr'] >= 0.8) & (df_roc['fpr'] <= 0.9)]
plot4 = (ggplot(df_roc, aes(x='fpr', y='tpr')) 
         + geom_line() 
# r2py:entity:geom_polygon_auc_3
         + geom_polygon(data=df_se, aes(x='fpr', y='tpr'), fill="red", alpha=0.3))
print(plot4)