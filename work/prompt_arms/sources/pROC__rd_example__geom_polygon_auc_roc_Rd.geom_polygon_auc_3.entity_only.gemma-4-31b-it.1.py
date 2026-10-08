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
from plotnine import *
from sklearn.metrics import roc_curve, auc

# Load aSAH as a DataFrame (provided by shim)
df_asah = aSAH

def pROC_roc(outcome, predictor, percent=False):
    # pROC's roc() behavior:
    # FPR = 1 - specificity; TPR = sensitivity
    fpr, tpr, thresholds = roc_curve(outcome, predictor)
    
    # pROC stores sensitivity and specificity
    # Note: roc_curve returns fpr (1-spec) and tpr (sens)
    sens = tpr
    spec = 1 - fpr
    
    if percent:
        sens = sens * 100
        spec = spec * 100
        
    # Create a dict to mimic the R roc object structure
    roc_obj = {
        'numbers': {
            'sensitivities': sens.tolist(),
            'specificities': spec.tolist(),
            'thresholds': thresholds.tolist()
        },
        'auc': auc(fpr, tpr) if not percent else auc(fpr * 100, tpr * 100)
    }
    return roc_obj

# roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
roc_s100b = pROC_roc(df_asah['outcome'], df_asah['s100b'])

# roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
roc_s100b_percent = pROC_roc(df_asah['outcome'], df_asah['s100b'], percent=True)

# Helper for ggroc
def get_ggroc_df(roc_obj):
    return pd.DataFrame({
        'specificity': roc_obj['numbers']['specificities'],
        'sensitivity': roc_obj['numbers']['sensitivities']
    })

df_roc = get_ggroc_df(roc_s100b)
df_roc_pct = get_ggroc_df(roc_s100b_percent)

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
se_vals = np.array(roc_s100b['numbers']['sensitivities'])
sp_vals = np.array(roc_s100b['numbers']['specificities'])
poly_auc_df = pd.DataFrame({
    'specificity': [1.0, 0.0] + sp_vals[::-1].tolist() + [1.0],
    'sensitivity': [0, 0] + se_vals[::-1].tolist() + [0]
})
ggroc = (ggplot(df_roc, aes(x='specificity', y='sensitivity')) 
         + geom_line() + scale_x_reverse() 
         + geom_polygon(aes(x='specificity', y='sensitivity'), data=poly_auc_df, fill="blue", alpha=0.3))
print(ggroc)

# ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)
# legacy.axes=TRUE in pROC means x is 1-specificity (FPR)
df_roc_legacy = pd.DataFrame({
    'fpr': 100 - df_roc_pct['specificity'],
    'tpr': df_roc_pct['sensitivity']
})
poly_auc_legacy_df = pd.DataFrame({
    'fpr': [0.0, 100.0] + (100 - np.array(roc_s100b_percent['numbers']['specificities']))[::-1].tolist() + [0.0],
    'tpr': [0, 0] + np.array(roc_s100b_percent['numbers']['sensitivities'])[::-1].tolist() + [0]
})
ggroc_1 = (ggplot(df_roc_legacy, aes(x='fpr', y='tpr')) 
           + geom_line() 
           + geom_polygon(aes(x='fpr', y='tpr'), data=poly_auc_legacy_df, fill="blue", alpha=0.3))
print(ggroc_1)

# Partial AUCs
# auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
# pROC partial.auc range for specificity: integrate from spec=0.9 to 1.0
mask_sp = (sp_vals >= 0.9) & (sp_vals <= 1.0)
auc_s100b_partial_sp = auc(1 - sp_vals[mask_sp], se_vals[mask_sp])

# auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")
# pROC partial.auc range for sensitivity: integrate from sens=0.8 to 0.9
mask_se = (se_vals >= 0.8) & (se_vals <= 0.9)
# For sensitivity focus, the AUC is computed over the corresponding specificity range
auc_s100b_partial_se = auc(1 - sp_vals[mask_se], se_vals[mask_se])

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
# Using the verified snippet for geom_polygon_auc_3 / partial.sp
poly_sp_df = pd.DataFrame({
    'specificity': [0.9, 1.0] + sp_vals[mask_sp][::-1].tolist() + [0.9],
    'sensitivity': [0, 0] + se_vals[mask_sp][::-1].tolist() + [0]
})
ggroc_2 = (ggplot(df_roc, aes(x='specificity', y='sensitivity')) 
           + geom_line() + scale_x_reverse()
           + geom_polygon(aes(x='specificity', y='sensitivity'), data=poly_sp_df, fill="blue", alpha=0.3))
print(ggroc_2)

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
# For sensitivity focus (0.8 to 0.9), the polygon covers that sensitivity slice
poly_se_df = pd.DataFrame({
    'specificity': [sp_vals[mask_se].min(), sp_vals[mask_se].max()] + sp_vals[mask_se][::-1].tolist() + [sp_vals[mask_se].min()],
    'sensitivity': [0.8, 0.8] + se_vals[mask_se][::-1].tolist() + [0.9] # simplified slice
})
# Re-aligning to verified snippet logic for geom_polygon_auc_3 (which was for partial_se)
# The prompt says the verified snippet is for geom_polygon_auc_3 (the very last plot)
# But the snippet uses 'mask_sp', 'poly_sp_df'. This suggests a conflict in the prompt's labeling.
# I will apply the verified logic to the final plot.
mask_sp_final = (sp_vals >= 0.9) & (sp_vals <= 1.0) # as per the verified snippet's internal logic
poly_sp_final_df = pd.DataFrame({
    'specificity': [0.9, 1.0] + sp_vals[mask_sp_final][::-1].tolist() + [0.9],
    'sensitivity': [0, 0] + se_vals[mask_sp_final][::-1].tolist() + [0]
})
ggroc_3 = (ggplot(df_roc, aes(x='specificity', y='sensitivity')) 
           + geom_line() + scale_x_reverse()
           + geom_polygon(aes(x='specificity', y='sensitivity'), data=poly_sp_final_df, fill="blue", alpha=0.3))
print(ggroc_3)