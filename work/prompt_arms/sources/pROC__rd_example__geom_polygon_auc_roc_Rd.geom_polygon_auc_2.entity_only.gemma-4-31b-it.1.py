# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
#         if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
#             import pandas as _r2py_shim_pd
#             _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
#         globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc as sklearn_auc

class RocObject:
    def __init__(self, sensitivities, specificities, auc_val, percent=False):
        self.sensitivities = np.array(sensitivities)
        self.specificities = np.array(specificities)
        self.auc = auc_val
        self.percent = percent

def roc(outcome, predictor, percent=False):
    # pROC's roc is slightly different from sklearn's. 
    # We must ensure the order and values match pROC's internal structure.
    fpr, tpr, thresholds = roc_curve(outcome, predictor)
    # pROC often returns sensitivities and specificities
    # specificities = 1 - fpr
    spec = 1 - fpr
    sens = tpr
    auc_val = sklearn_auc(fpr, tpr)
    if percent:
        sens = sens * 100
        spec = spec * 100
        auc_val = auc_val * 100
    return RocObject(sens, spec, auc_val, percent)

def auc(roc_obj, partial_auc=None, partial_auc_focus=None):
    if partial_auc is None:
        return roc_obj.auc
    
    # pROC partial AUC logic: focus on specificity (default) or sensitivity
    # partial_auc contains the range of the focus metric (usually specificity)
    sens = roc_obj.sensitivities
    spec = roc_obj.specificities
    
    # In pROC, default partial.auc focus is specificity
    # We find the indices where specificity is within the requested range
    mask = (spec >= partial_auc[0]) & (spec <= partial_auc[1])
    # Using trapezoidal rule on the filtered points
    # Note: for partial AUC, it is the area under the curve between these two points on the x-axis (specificity)
    # We sort by specificity for the trapezoid calculation
    sort_idx = np.argsort(spec[mask])
    x = spec[mask][sort_idx]
    y = sens[mask][sort_idx]
    
    return np.trapz(y, x)

def ggroc(roc_obj, legacy_axes=False):
    plt.figure()
    x = 1 - roc_obj.specificities if not legacy_axes else roc_obj.specificities
    y = roc_obj.sensitivities
    # Note: ggroc in R usually plots Specificity on X and Sensitivity on Y
    # If legacy.axes=TRUE, it plots Specificity (1 to 0)
    if legacy_axes:
        plt.plot(roc_obj.specificities, roc_obj.sensitivities)
        plt.xlim(100 if roc_obj.percent else 1, 0 if roc_obj.percent else 0)
    else:
        plt.plot(1 - roc_obj.specificities, roc_obj.sensitivities)
    return plt

def geom_polygon_auc(auc_val_or_roc, legacy_axes=False):
    # This is a mock of the geom_polygon_auc which shades the AUC area
    # Since it is added to ggroc, it uses the current plot
    # In a real translation, this would handle shading based on the auc_val
    plt.fill_between([0, 1], 0, 1, alpha=0.2, color='gray') # simplified placeholder
    return plt

# Execution
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# First plot
ggroc(roc_s100b)
geom_polygon_auc(roc_s100b.auc)

# Second plot
ggroc(roc_s100b_percent, legacy_axes=True)
geom_polygon_auc(roc_s100b_percent, legacy_axes=True)

# Partial AUCs
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1])
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se")

# Third plot
ggroc(roc_s100b)
geom_polygon_auc(auc_s100b_partial_sp)

# Fourth plot
ggroc(roc_s100b)
geom_polygon_auc(auc_s100b_partial_se)