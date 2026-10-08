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

import warnings
warnings.filterwarnings('ignore')

from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri, r
import rpy2.robjects as ro

pandas2ri.activate()

# Import pROC and ggplot2
proc = importr('pROC')
ggplot2 = importr('ggplot2')

# Convert aSAH to R dataframe
aSAH_r = pandas2ri.py2rpy(aSAH)

# Create ROC curves
roc_s100b = proc.roc(aSAH_r.rx2('outcome'), aSAH_r.rx2('s100b'))
roc_s100b_percent = proc.roc(aSAH_r.rx2('outcome'), aSAH_r.rx2('s100b'), percent=True)

# Plot 1: ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
r('suppressPackageStartupMessages(library(pROC))')
r('library(ggplot2)')

r_code_1 = '''
ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
'''
ro.r.assign('roc.s100b', roc_s100b)
ro.r(r_code_1)

# Plot 2: ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
r_code_2 = '''
ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
'''
ro.r.assign('roc.s100b.percent', roc_s100b_percent)
ro.r(r_code_2)

# Partial AUCs
auc_s100b_partial_sp = proc.auc(roc_s100b, **{'partial.auc': ro.FloatVector([0.9, 1])})
auc_s100b_partial_se = proc.auc(roc_s100b, **{'partial.auc': ro.FloatVector([0.8, 0.9]), 'partial.auc.focus': 'se'})

# Store as Python variables for comparison
auc_s100b_partial_sp = float(auc_s100b_partial_sp[0])
auc_s100b_partial_se = float(auc_s100b_partial_se[0])

# Plot 3: ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
r_code_3 = '''
ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
'''
ro.r.assign('auc.s100b.partial.sp', ro.FloatVector([auc_s100b_partial_sp]))
ro.r(r_code_3)

# Plot 4: ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
r_code_4 = '''
ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
'''
ro.r.assign('auc.s100b.partial.se', ro.FloatVector([auc_s100b_partial_se]))
ro.r(r_code_4)
