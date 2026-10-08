# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyroc import roc, auc

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

# Create a ROC curve:
# data(aSAH)  # Already loaded by data shim
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'])
roc_s100b_percent = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)
fig1, ax1 = plt.subplots()
ax1.plot(1 - np.array(roc_s100b['specificities']), np.array(roc_s100b['sensitivities']))
ax1.set_xlabel('1 - Specificity')
ax1.set_ylabel('Sensitivity')
ax1.set_title(f"ROC Curve (AUC = {roc_s100b['auc']:.4f})")
plt.show()

# legacy.axes must be repeated
fig2, ax2 = plt.subplots()
ax2.plot(np.array(roc_s100b_percent['specificities']), np.array(roc_s100b_percent['sensitivities']))
ax2.set_xlabel('Specificity')
ax2.set_ylabel('Sensitivity')
ax2.set_title(f"ROC Curve - Percent (AUC = {roc_s100b_percent['auc']:.4f})")
plt.show()

# Partial AUCs
auc_s100b_partial_sp = auc(roc_s100b, partial_auc=[0.9, 1])
auc_s100b_partial_se = auc(roc_s100b, partial_auc=[0.8, 0.9], partial_auc_focus="se")

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
sp_vals = np.array(roc_s100b['specificities'])
se_vals = np.array(roc_s100b['sensitivities'])
fig3, ax3 = plt.subplots()
ax3.plot(1 - sp_vals, se_vals)
ax3.fill_between(1 - sp_vals[(sp_vals >= 0.9) & (sp_vals <= 1)], 
                  0, 
                  se_vals[(sp_vals >= 0.9) & (sp_vals <= 1)], 
                  alpha=0.3, label=f'Partial AUC = {auc_s100b_partial_sp:.4f}')
ax3.set_xlabel('1 - Specificity')
ax3.set_ylabel('Sensitivity')
ax3.set_title('ROC Curve with Partial AUC (Specificity 0.9-1.0)')
ax3.legend()
plt.show()

# ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)
fig4, ax4 = plt.subplots()
ax4.plot(1 - sp_vals, se_vals)
ax4.fill_between(1 - sp_vals[(sp_vals >= 0.8) & (sp_vals <= 0.9)], 
                  0, 
                  se_vals[(sp_vals >= 0.8) & (sp_vals <= 0.9)], 
                  alpha=0.3, label=f'Partial AUC = {auc_s100b_partial_se:.4f}')
ax4.set_xlabel('1 - Specificity')
ax4.set_ylabel('Sensitivity')
ax4.set_title('ROC Curve with Partial AUC (Sensitivity 0.8-0.9)')
ax4.legend()
plt.show()
