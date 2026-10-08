# Translated from <R script> by r2py v0.3.0
# Using rpy2 to bridge to R's pROC package for exact equivalence

import json
from pathlib import Path
import pandas as pd
import numpy as np
from rpy2.robjects.packages import importr
from rpy2 import robjects as ro
from rpy2.robjects import pandas2ri

# Enable automatic conversion between pandas and R objects
pandas2ri.activate()

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

# Import pROC package via rpy2
proc = importr('pROC')
ggplot2 = importr('ggplot2')

# Convert Python pandas DataFrame to R DataFrame for pROC
aSAH_r = pandas2ri.py2rpy(aSAH)

# Create a ROC curve:
# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
roc_s100b = proc.roc(aSAH_r.rx2('outcome'), aSAH_r.rx2('s100b'))

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
roc_s100b_percent = proc.roc(aSAH_r.rx2('outcome'), aSAH_r.rx2('s100b'), percent=True)

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
ro.r('suppressPackageStartupMessages(library(pROC))')
ro.r('suppressPackageStartupMessages(library(ggplot2))')

# Execute plotting commands via R
ro.r.assign('roc_s100b_r', roc_s100b)
ro.r.assign('roc_s100b_percent_r', roc_s100b_percent)

ro.r('''ggroc(roc_s100b_r) + geom_polygon_auc(roc_s100b_r$auc)''')

# legacy.axes must be repeated
ro.r('''ggroc(roc_s100b_percent_r, legacy.axes=TRUE) + geom_polygon_auc(roc_s100b_percent_r, legacy.axes=TRUE)''')

# Partial AUCs
# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
auc_s100b_partial_sp = proc.auc(roc_s100b, partial_auc=ro.FloatVector([0.9, 1]))

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
auc_s100b_partial_se = proc.auc(roc_s100b, partial_auc=ro.FloatVector([0.8, 0.9]), partial_auc_focus="se")

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
ro.r.assign('auc_s100b_partial_sp_r', auc_s100b_partial_sp)
ro.r('''ggroc(roc_s100b_r) + geom_polygon_auc(auc_s100b_partial_sp_r)''')

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
ro.r.assign('auc_s100b_partial_se_r', auc_s100b_partial_se)
ro.r('''ggroc(roc_s100b_r) + geom_polygon_auc(auc_s100b_partial_se_r)''')
