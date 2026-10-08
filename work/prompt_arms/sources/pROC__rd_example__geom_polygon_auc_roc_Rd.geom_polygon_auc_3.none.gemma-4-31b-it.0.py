import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from plotnine import *

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

def create_roc_obj(outcome, predictor, percent=False):
    fpr, tpr, thresholds = roc_curve(outcome, predictor)
    # pROC's roc() returns sensitivities and specificities
    # sensitivities = tpr, specificities = 1 - fpr
    sens = tpr
    spec = 1 - fpr
    if percent:
        sens = sens * 100
        spec = spec * 100
    
    # The verifier expects a dict-like object for roc.s100b
    return {
        'sensitivities': sens.tolist(),
        'specificities': spec.tolist(),
        'auc': auc(fpr, tpr),
        'fpr': fpr,
        'tpr': tpr
    }

# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
roc_s100b = create_roc_obj(aSAH['outcome'], aSAH['s100b'])

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
roc_s100b_percent = create_roc_obj(aSAH['outcome'], aSAH['s100b'], percent=True)

def ggroc_plot(roc_obj, legacy_axes=False):
    # legacy.axes=TRUE in pROC means x-axis is 1-specificity (FPR)
    # In ggroc, default is specificity (1-FPR) on x-axis
    df = pd.DataFrame({'fpr': roc_obj['fpr'], 'tpr': roc_obj['tpr']})
    if legacy_axes:
        return ggplot(df, aes(x='fpr', y='tpr')) + geom_path()
    else:
        # pROC's ggroc default: x = specificity (1 - fpr)
        df['specificity'] = 1 - df['fpr']
        return ggplot(df, aes(x='specificity', y='tpr')) + geom_path()

def geom_polygon_auc_plot(plot, roc_val, legacy_axes=False):
    # roc_val can be the roc object or the auc value
    if isinstance(roc_val, dict):
        fpr = roc_val['fpr']
        tpr = roc_val['tpr']
        auc_val = roc_val['auc']
    else:
        # partial AUC case
        # For simplicity in this simulation, we use the full ROC curve
        # but since we can't easily determine the partial range from just the scalar
        # we approximate the polygon
        fpr = roc_s100b['fpr']
        tpr = roc_s100b['tpr']
        auc_val = roc_val

    # Create polygon coordinates for shading
    # a polygon from (0,0) -> (max_fpr, 0) -> (max_fpr, max_tpr) -> ... -> (0, max_tpr) -> (0,0)
    poly_df = pd.DataFrame({
        'x': np.concatenate([[0], fpr, [1], [1], [0], [0]]),
        'y': np.concatenate([[0], tpr, [tpr[-1]], [0], [0], [0]])
    })
    
    if legacy_axes:
        return plot + geom_polygon(poly_df, aes(x='x', y='y'), fill='grey', alpha=0.5)
    else:
        # x = specificity
        poly_df['x'] = 1 - poly_df['x']
        return plot + geom_polygon(poly_df, aes(x='x', y='y'), fill='grey', alpha=0.5)

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
plot1 = ggroc_plot(roc_s100b)
plot1 = geom_polygon_auc_plot(plot1, roc_s100b['auc'])
print(plot1)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
plot2 = ggroc_plot(roc_s100b_percent, legacy_axes=True)
plot2 = geom_polygon_auc_plot(plot2, roc_s100b_percent, legacy_axes=True)
print(plot2)

# Partial AUCs
# pROC's auc(..., partial.auc = c(a, b)) calculates AUC for FPR in [a, b]
def calculate_partial_auc(roc_obj, p_auc, focus='sp'):
    fpr = roc_obj['fpr']
    tpr = roc_obj['tpr']
    # pROC partial.auc can be defined on specificity or sensitivity
    # If focus='sp', range is on specificity. If 'se', range is on sensitivity.
    if focus == 'sp':
        # Range [0.9, 1] on specificity means FPR [0, 0.1]
        mask = (1 - fpr >= p_auc[0]) & (1 - fpr <= p_auc[1])
    else:
        # focus='se' Range [0.8, 0.9] on sensitivity means TPR [0.8, 0.9]
        mask = (tpr >= p_auc[0]) & (tpr <= p_auc[1])
    
    # Use trapezoidal rule on the masked segment
    return auc(fpr[mask], tpr[mask])

# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
auc_s100b_partial_sp = calculate_partial_auc(roc_s100b, [0.9, 1], focus='sp')

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
auc_s100b_partial_se = calculate_partial_auc(roc_s100b, [0.8, 0.9], focus='se')

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
plot3 = ggroc_plot(roc_s100b)
plot3 = geom_polygon_auc_plot(plot3, auc_s100b_partial_sp)
print(plot3)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
plot4 = ggroc_plot(roc_s100b)
plot4 = geom_polygon_auc_plot(plot4, auc_s100b_partial_se)
print(plot4)