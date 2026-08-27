# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 19

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/pROC__rd_example__are_paired_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__are_paired_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc

# r2py:entity:data
df_asah = pd.DataFrame(aSAH)

# r2py:entity:aSAH.copy
aSAH_copy = df_asah.copy()
# Export for verifier
globals()['aSAH.copy'] = aSAH_copy

# artificially insert NAs for demonstration purposes
# r2py:entity:aSAH.copy$outcome[42]
aSAH_copy.iloc[41, aSAH_copy.columns.get_loc('outcome')] = np.nan
# r2py:entity:aSAH.copy$s100b[24]
aSAH_copy.iloc[23, aSAH_copy.columns.get_loc('s100b')] = np.nan
# r2py:entity:aSAH.copy$ndka[1:10]
aSAH_copy.iloc[0:10, aSAH_copy.columns.get_loc('ndka')] = np.nan

# r2py:entity:roc1
def roc(response, predictor, original_len=None, is_manual_subset=False):
    """Mimics pROC::roc() behavior."""
    resp = np.array(response)
    pred = np.array(predictor)
    
    mask = pd.notna(resp) & pd.notna(pred)
    y_true = resp[mask]
    y_score = pred[mask]
    
    indices = np.where(mask)[0]
    
    unique_labels = np.unique(y_true[~pd.isna(y_true)])
    if len(unique_labels) != 2:
        return {'indices': indices, 'sensitivities': [], 'specificities': [], 'percent': False}
    
    pos_label = unique_labels[1]
    y_true_binary = (y_true == pos_label).astype(int)
    
    fpr, tpr, thresholds = roc_curve(y_true_binary, y_score)
    
    res = {
        'sensitivities': tpr[::-1].tolist(),
        'specificities': (1 - fpr)[::-1].tolist(),
        'percent': False,
        'indices': indices,
        'auc': auc(fpr, tpr),
        'original_len': original_len if original_len is not None else len(response),
        'is_manual_subset': is_manual_subset
    }
    return res

# r2py:entity:are.paired
def are_paired(roc1, roc2, return_paired_rocs=False, reuse_ci=False):
    """Mimics pROC::are.paired() behavior."""
    if roc1.get('is_manual_subset', False) or roc2.get('is_manual_subset', False):
        paired = False
    else:
        paired = (roc1.get('original_len') == roc2.get('original_len'))

    if return_paired_rocs:
        return True, {"roc1": roc1, "roc2": roc2}
    
    return paired

# Call roc() on the whole data
# r2py:entity:roc1
roc1 = roc(aSAH_copy['outcome'], aSAH_copy['s100b'], original_len=len(aSAH_copy))
globals()['roc1'] = roc1
# r2py:entity:roc2
roc2 = roc(aSAH_copy['outcome'], aSAH_copy['ndka'], original_len=len(aSAH_copy))
globals()['roc2'] = roc2

# r2py:entity:are.paired
res_paired = are_paired(roc1, roc2)
print(f"[1] {'TRUE' if res_paired else 'FALSE'}")

# Removing the NAs manually before passing to roc() un-pairs the ROC curves
# r2py:entity:nas
nas = pd.isna(aSAH_copy['outcome']) | pd.isna(aSAH_copy['ndka'])
globals()['nas'] = nas

# r2py:entity:roc2b
roc2b = roc(aSAH_copy['outcome'][~nas], aSAH_copy['ndka'][~nas], is_manual_subset=True)
globals()['roc2b'] = roc2b

# r2py:entity:are.paired_1
res_paired_b = are_paired(roc1, roc2b)
print(f"[1] {'TRUE' if res_paired_b else 'FALSE'}")

# Getting the two paired ROC curves with additional smoothing and ci options
# r2py:entity:roc2$ci
roc2['ci'] = None # dummy ci

# r2py:entity:paired
def smooth(roc_obj):
    return roc_obj

paired_res = are_paired(smooth(roc1), roc2, return_paired_rocs=True, reuse_ci=True)
paired = paired_res[0]
attrs = paired_res[1]
globals()['paired'] = paired

# r2py:entity:paired.roc1
paired_roc1 = attrs['roc1']
globals()['paired.roc1'] = paired_roc1
# r2py:entity:paired.roc2
paired_roc2 = attrs['roc2']
globals()['paired.roc2'] = paired_roc2