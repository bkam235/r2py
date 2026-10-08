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

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
import pandas as pd

# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages(library(pROC))
proc = importr('pROC')

# r2py:entity:import_pROC
# (library pROC already imported above)

# r2py:entity:data
# data(aSAH) - aSAH is already loaded from data shim
aSAH_r = robjects.DataFrame({
    'outcome': robjects.StrVector(aSAH['outcome']),
    'gender': robjects.StrVector(aSAH['gender']),
    'age': robjects.IntVector(aSAH['age']),
    'wfns': robjects.StrVector(aSAH['wfns']),
    's100b': robjects.FloatVector(aSAH['s100b']),
    'gos6': robjects.StrVector(aSAH['gos6']),
    'ndka': robjects.FloatVector(aSAH['ndka'])
})

# r2py:entity:roc.s100b
# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
roc_s100b = proc.roc(aSAH_r.rx2('outcome'), aSAH_r.rx2('s100b'))

# r2py:entity:roc.s100b.percent
# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
roc_s100b_percent = proc.roc(aSAH_r.rx2('outcome'), aSAH_r.rx2('s100b'), percent=True)

# r2py:entity:ggroc
# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
proc.ggroc(roc_s100b) + proc.geom_polygon_auc(roc_s100b.rx2('auc'))

# r2py:entity:geom_polygon_auc
# (included in above)

# r2py:entity:ggroc_1
# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
proc.ggroc(roc_s100b_percent, legacy_axes=True) + proc.geom_polygon_auc(roc_s100b_percent, legacy_axes=True)

# r2py:entity:geom_polygon_auc_1
# (included in above)

# r2py:entity:auc.s100b.partial.sp
# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
auc_s100b_partial_sp = proc.auc(roc_s100b, partial_auc=robjects.FloatVector([0.9, 1.0]))

# r2py:entity:auc.s100b.partial.se
# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
auc_s100b_partial_se = proc.auc(roc_s100b, partial_auc=robjects.FloatVector([0.8, 0.9]), partial_auc_focus='se')

# r2py:entity:ggroc_2
# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
proc.ggroc(roc_s100b) + proc.geom_polygon_auc(auc_s100b_partial_sp)

# r2py:entity:geom_polygon_auc_2
# (included in above)

# r2py:entity:ggroc_3
# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
proc.ggroc(roc_s100b) + proc.geom_polygon_auc(auc_s100b_partial_se)

# r2py:entity:geom_polygon_auc_3
# (included in above)
