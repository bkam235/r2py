# Translated from R by r2py
# Model: openrouter:google/gemma-4-31b-it

import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# r2py:data_shim:begin
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__geom_polygon_auc_roc_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['aSAH']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            _r2py_shim_v = pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

try:
    from proclite import roc as proclite_roc
    from proclite import auc as proclite_auc
except ImportError:
    # Fallback: use sklearn for ROC computation
    from sklearn.metrics import roc_curve, auc as sklearn_auc
    proclite_roc = None

# Create a ROC curve:
aSAH_df = pd.DataFrame(aSAH) if isinstance(aSAH, dict) else aSAH

if proclite_roc:
    roc_s100b = proclite_roc(aSAH_df['outcome'], aSAH_df['s100b'])
    roc_s100b_percent = proclite_roc(aSAH_df['outcome'], aSAH_df['s100b'], percent=True)
else:
    # Fallback using sklearn
    from sklearn.metrics import roc_curve, auc as sklearn_auc
    fpr, tpr, _ = roc_curve(aSAH_df['outcome'], aSAH_df['s100b'])
    roc_s100b = {'fpr': fpr, 'tpr': tpr, 'auc': sklearn_auc(fpr, tpr)}
    roc_s100b_percent = {'fpr': fpr * 100, 'tpr': tpr * 100, 'auc': sklearn_auc(fpr * 100, tpr * 100)}

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
fig1, ax1 = plt.subplots()
if isinstance(roc_s100b, dict):
    ax1.plot(roc_s100b['fpr'], roc_s100b['tpr'])
ax1.set_xlabel('1 - Specificity')
ax1.set_ylabel('Sensitivity')
ax1.set_title(f"ROC Curve - AUC: {roc_s100b['auc'] if isinstance(roc_s100b, dict) else roc_s100b.auc:.4f}")
plt.show()

# legacy.axes must be repeated
fig2, ax2 = plt.subplots()
if isinstance(roc_s100b_percent, dict):
    ax2.plot(roc_s100b_percent['fpr'], roc_s100b_percent['tpr'])
ax2.set_xlabel('100 - Specificity (%)')
ax2.set_ylabel('Sensitivity (%)')
ax2.set_title(f"ROC Curve (%) - AUC: {roc_s100b_percent['auc'] if isinstance(roc_s100b_percent, dict) else roc_s100b_percent.auc:.4f}")
plt.show()

# Partial AUCs
if proclite_roc:
    auc_s100b_partial_sp = proclite_auc(roc_s100b, partial_auc=[0.9, 1])
    auc_s100b_partial_se = proclite_auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se")
else:
    # Approximate partial AUC from sklearn ROC
    def calc_partial_auc(fpr, tpr, sp_range):
        mask = (fpr >= sp_range[0]) & (fpr <= sp_range[1])
        if np.sum(mask) > 1:
            return sklearn_auc(fpr[mask], tpr[mask])
        return 0.0
    auc_s100b_partial_sp = calc_partial_auc(fpr, tpr, [0.9, 1.0])
    auc_s100b_partial_se = calc_partial_auc(fpr, tpr, [0.8, 0.9])

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
fig3, ax3 = plt.subplots()
if isinstance(roc_s100b, dict):
    ax3.plot(roc_s100b['fpr'], roc_s100b['tpr'])
ax3.set_xlabel('1 - Specificity')
ax3.set_ylabel('Sensitivity')
ax3.set_title(f"ROC with Partial AUC (0.9-1.0): {auc_s100b_partial_sp:.4f}")
plt.show()

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
fig4, ax4 = plt.subplots()
if isinstance(roc_s100b, dict):
    ax4.plot(roc_s100b['fpr'], roc_s100b['tpr'])
ax4.set_xlabel('1 - Specificity')
ax4.set_ylabel('Sensitivity')
ax4.set_title(f"ROC with Partial AUC (0.8-0.9): {auc_s100b_partial_se:.4f}")
plt.show()
