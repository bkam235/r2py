# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/pROC__rd_example__geom_polygon_auc_roc_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end
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

import pandas as pd
import numpy as np
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri, FloatVector, IntVector
from plotnine import *

pandas2ri.activate()

# r2py:entity:suppressPackageStartupMessages
pROC = importr('pROC')

# r2py:entity:data
# aSAH is loaded by the data shim above

# Convert pandas DataFrame columns to R vectors for pROC functions
outcome_r = IntVector(aSAH['outcome'].astype(int).values)
s100b_r = FloatVector(aSAH['s100b'].values)

# r2py:entity:roc.s100b
roc_s100b = pROC.roc(outcome_r, s100b_r)

# r2py:entity:roc.s100b.percent
roc_s100b_percent = pROC.roc(outcome_r, s100b_r, percent=True)

# r2py:entity:ggroc
# r2py:entity:geom_polygon_auc
plot_1 = pROC.ggroc(roc_s100b)
plot_1_with_auc = plot_1 + pROC.geom_polygon_auc(roc_s100b)

# r2py:entity:ggroc_1
# r2py:entity:geom_polygon_auc_1
plot_2 = pROC.ggroc(roc_s100b_percent, legacy_axes=True)
plot_2_with_auc = plot_2 + pROC.geom_polygon_auc(roc_s100b_percent, legacy_axes=True)

# r2py:entity:auc.s100b.partial.sp
auc_s100b_partial_sp = pROC.auc(roc_s100b, partial_auc=FloatVector([0.9, 1.0]))

# r2py:entity:auc.s100b.partial.se
auc_s100b_partial_se = pROC.auc(roc_s100b, partial_auc=FloatVector([0.8, 0.9]), partial_auc_focus='se')

# r2py:entity:ggroc_2
# r2py:entity:geom_polygon_auc_2
plot_3 = pROC.ggroc(roc_s100b)
plot_3_with_auc = plot_3 + pROC.geom_polygon_auc(auc_s100b_partial_sp)

# r2py:entity:ggroc_3
# r2py:entity:geom_polygon_auc_3
plot_4 = pROC.ggroc(roc_s100b)
plot_4_with_auc = plot_4 + pROC.geom_polygon_auc(auc_s100b_partial_se)
