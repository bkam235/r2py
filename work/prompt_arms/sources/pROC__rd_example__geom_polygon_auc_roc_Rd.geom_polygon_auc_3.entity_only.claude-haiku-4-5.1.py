# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

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

from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import importr
import pandas as pd
import numpy as np

# Enable automatic conversion between R and pandas
pandas2ri.activate()

# r2py:entity:suppressPackageStartupMessages
r('suppressPackageStartupMessages(library(pROC))')

# r2py:entity:import_pROC
# pROC is imported via R's library call above

# r2py:entity:data
# aSAH is already loaded via data shim
aSAH_r = pandas2ri.py2rpy(aSAH)
r.assign('aSAH', aSAH_r)

# r2py:entity:roc.s100b
r('roc.s100b <- roc(aSAH$outcome, aSAH$s100b)')
roc_s100b = r('roc.s100b')

# r2py:entity:roc.s100b.percent
r('roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)')
roc_s100b_percent = r('roc.s100b.percent')

# r2py:entity:ggroc
# r2py:entity:geom_polygon_auc
r('ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)')

# r2py:entity:ggroc_1
# r2py:entity:geom_polygon_auc_1
r('ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)')

# r2py:entity:auc.s100b.partial.sp
r('auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))')
auc_s100b_partial_sp = r('auc.s100b.partial.sp')

# r2py:entity:auc.s100b.partial.se
r('auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")')
auc_s100b_partial_se = r('auc.s100b.partial.se')

# r2py:entity:ggroc_2
# r2py:entity:geom_polygon_auc_2
r('ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)')

# r2py:entity:ggroc_3
# r2py:entity:geom_polygon_auc_3
r('ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)')
