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

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc as sklearn_auc
from plotnine import *

# Define a simple class to mimic pROC's roc object
class RocObject:
    def __init__(self, sensitivities, specificities, auc_val):
        self.sensitivities = sensitivities
        self.specificities = specificities
        self.auc = auc_val

def roc(outcome, predictor, percent=False):
    fpr, tpr, thresholds = roc_curve(outcome, predictor)
    # pROC sensitivities and specificities are usually sorted by threshold
    # roc_curve returns fpr in increasing order.
    # Specificity = 1 - FPR
    spec = 1 - fpr
    sens = tpr
    auc_val = sklearn_auc(fpr, tpr)
    
    if percent:
        sens = sens * 100
        spec = spec * 100
        # AUC for percent scales by 100*100? No, pROC's percent=TRUE 
        # scales axes, but AUC is typically 0-1 or 0-100 depending on version.
        # Actually, pROC's auc() function calculates AUC based on the provided ROC.
        # If axes are 0-100, AUC is usually still represented as 0-1 or 0-100.
        # Given the R output, we just need the object structure.
        pass 
    
    return RocObject(sens, spec, auc_val)

def auc(roc_obj, partial_auc=None, partial_auc_focus=None):
    if partial_auc is None:
        return roc_obj.auc
    
    # Partial AUC implementation
    sens = np.array(roc_obj.sensitivities)
    spec = np.array(roc_obj.specificities)
    
    if partial_auc_focus == "se":
        # Focus on sensitivity range
        mask = (sens >= partial_auc[0]) & (sens <= partial_auc[1])
    else:
        # Focus on specificity range (default)
        mask = (spec >= partial_auc[0]) & (spec <= partial_auc[1])
        
    # Using trapezoidal rule for partial AUC
    # Since we want the area under the curve in that specific range:
    # If focus is specificity, x is specificity, y is sensitivity.
    # we must ensure we are integrating along the correct axis.
    x = spec[mask]
    y = sens[mask]
    
    # Sorting is required for sklearn.metrics.auc
    idx = np.argsort(x)
    return sklearn_auc(x[idx], y[idx])

# Create a ROC curve:
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# Visualization helper
def ggroc(roc_obj, legacy_axes=False):
    df = pd.DataFrame({'sensitivity': roc_obj.sensitivities, 'specificity': roc_obj.specificities})
    if legacy_axes:
        # legacy.axes=TRUE in ggroc means x-axis is specificity (1 to 0)
        return ggplot(df, aes(x='specificity', y='sensitivity')) + geom_line() + scale_x_reverse()
    else:
        # Default ggroc x-axis is specificity (0 to 1) or sensitivity? 
        # Actually ggroc defaults to specificity on x-axis.
        return ggplot(df, aes(x='specificity', y='sensitivity')) + geom_line()

def geom_polygon_auc(roc_or_auc, legacy_axes=False):
    # This is a simplified approximation of pROC's geom_polygon_auc
    # In the R source, it's used as a layer.
    if isinstance(roc_or_auc, (float, np.float64)):
        # Handle partial AUC value
        return geom_polygon(aes(x='specificity', y='sensitivity'), 
                            data=pd.DataFrame({'specificity':[0,1,1,0], 'sensitivity':[0,0,1,1]}), # placeholder
                            fill="blue", alpha=0.3)
    
    # If it's a roc object, polygon the whole thing
    df = pd.DataFrame({'specificity': roc_or_auc.specificities, 'sensitivity': roc_or_auc.sensitivities})
    # Close the polygon
    poly_df = pd.DataFrame({
        'specificity': [1, 1] + df['specificity'].tolist() + [0, 0],
        'sensitivity': [0, 0] + df['sensitivity'].tolist() + [0, 0]
    })
    return geom_polygon(aes(x='specificity', y='sensitivity'), data=poly_df, fill="blue", alpha=0.3)

# Execute Plots
df_roc = pd.DataFrame({'sensitivity': roc_s100b.sensitivities, 'specificity': roc_s100b.specificities})
plot_1 = ggroc(roc_s100b) + geom_polygon_auc(roc_s100b)
print(plot_1)

plot_2 = ggroc(roc_s100b_percent, legacy_axes=True) + geom_polygon_auc(roc_s100b_percent, legacy_axes=True)
print(plot_2)

# Partial AUCs
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1])
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se")

# For these specific plots, we use the verified logic provided in the prompt
sp_vals = np.array(roc_s100b.specificities)
se_vals = np.array(roc_s100b.sensitivities)

mask_sp = (sp_vals >= 0.9) & (sp_vals <= 1.0)
poly_sp_df = pd.DataFrame({
    'specificity': [0.9, 1.0] + sp_vals[mask_sp][::-1].tolist() + [0.9],
    'sensitivity': [0, 0] + se_vals[mask_sp][::-1].tolist() + [0]
})
plot_3 = (ggplot(df_roc, aes(x='specificity', y='sensitivity')) 
          + geom_line() + scale_x_reverse()
          + geom_polygon(aes(x='specificity', y='sensitivity'), data=poly_sp_df, fill="blue", alpha=0.3))
print(plot_3)

mask_se = (se_vals >= 0.8) & (se_vals <= 0.9)
poly_se_df = pd.DataFrame({
    'specificity': [sp_vals[se_vals == 0.9][0], sp_vals[se_vals == 0.8][0]] + sp_vals[mask_se][::-1].tolist() + [sp_vals[se_vals == 0.9][0]],
    'sensitivity': [0.9, 0.8] + se_vals[mask_se][::-1].tolist() + [0.9]
})
# For the 4th plot, we use the logic from plot_3 but with the 'se' partial range
plot_4 = (ggplot(df_roc, aes(x='specificity', y='sensitivity')) 
          + geom_line() + scale_x_reverse()
          + geom_polygon(aes(x='specificity', y='sensitivity'), data=poly_se_df, fill="blue", alpha=0.3))
print(plot_4)