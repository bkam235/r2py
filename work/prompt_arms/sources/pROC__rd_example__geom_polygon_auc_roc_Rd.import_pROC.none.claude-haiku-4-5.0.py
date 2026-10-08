# Translated from <R script> by r2py v0.3.0
import json
from pathlib import Path

# r2py:data_shim:begin
import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['aSAH']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            import pandas as _r2py_shim_pd
            _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.pandas2ri as pandas2ri

# Enable automatic conversion between pandas and R
pandas2ri.activate()

# Import pROC package in R
robjects.r('suppressPackageStartupMessages(library(pROC))')

# Convert Python aSAH to R dataframe
aSAH_r = pandas2ri.py2rpy(aSAH)

# Create ROC curves
robjects.globalenv['aSAH'] = aSAH_r
roc_s100b = robjects.r('roc(aSAH$outcome, aSAH$s100b)')
roc_s100b_percent = robjects.r('roc(aSAH$outcome, aSAH$s100b, percent = TRUE)')

# Call ggroc + geom_polygon_auc
robjects.r('ggroc(roc(aSAH$outcome, aSAH$s100b)) + geom_polygon_auc(roc(aSAH$outcome, aSAH$s100b)$auc)')

# Legacy axes version
robjects.r('ggroc(roc(aSAH$outcome, aSAH$s100b, percent = TRUE), legacy.axes=TRUE) + geom_polygon_auc(roc(aSAH$outcome, aSAH$s100b, percent = TRUE), legacy.axes=TRUE)')

# Partial AUCs
auc_s100b_partial_sp = robjects.r('auc(roc(aSAH$outcome, aSAH$s100b), partial.auc = c(0.9, 1))')
auc_s100b_partial_se = robjects.r('auc(roc(aSAH$outcome, aSAH$s100b), partial.auc = c(0.8, 0.9), partial.auc.focus="se")')

# Convert back to Python
auc_s100b_partial_sp = float(auc_s100b_partial_sp[0])
auc_s100b_partial_se = float(auc_s100b_partial_se[0])

# Plot partial AUCs
robjects.r('ggroc(roc(aSAH$outcome, aSAH$s100b)) + geom_polygon_auc(auc(roc(aSAH$outcome, aSAH$s100b), partial.auc = c(0.9, 1)))')
robjects.r('ggroc(roc(aSAH$outcome, aSAH$s100b)) + geom_polygon_auc(auc(roc(aSAH$outcome, aSAH$s100b), partial.auc = c(0.8, 0.9), partial.auc.focus="se"))')
