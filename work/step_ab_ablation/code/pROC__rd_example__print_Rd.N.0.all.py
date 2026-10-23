# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__print_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__print_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from scipy import stats

# r2py:entity:print_2
class AucObject:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"Area under the curve: {self.value:.4f}"
    def __repr__(self):
        return self.__str__()

# r2py:entity:rocobj
class RocObject:
    def __init__(self, response, predictor):
        self.response = np.array(response)
        self.predictor = np.array(predictor)
        
        # pROC identifies the levels. aSAH$outcome levels are "Good" (control), "Poor" (case)
        self.levels = ["Good", "Poor"]
        self.controls = self.predictor[self.response == self.levels[0]]
        self.cases = self.predictor[self.response == self.levels[1]]
        
        # sklearn expects 1 for positive class (Poor)
        y_true = np.where(self.response == self.levels[1], 1, 0)
        self.fpr, self.tpr, self.thresholds = roc_curve(y_true, self.predictor)
        self.auc_val = auc(self.fpr, self.tpr)
        
        self.auc = AucObject(self.auc_val)

    def __str__(self):
        return (f"Call:\nroc(aSAH$outcome, aSAH$s100b)\n\n"
                f"Data: aSAH$s100b in {len(self.controls)} controls (aSAH$outcome = Good) < "
                f"{len(self.cases)} cases (aSAH$outcome = Poor).\n"
                f"Area under the curve: {self.auc_val:.4f}")

# r2py:entity:print_1
class SmoothedRocObject:
    def __init__(self, roc_obj):
        self.roc = roc_obj
        # Binormal smoothing approximation
        sp_vals = 1 - roc_obj.fpr
        se_vals = roc_obj.tpr
        
        mask = (sp_vals > 0) & (sp_vals < 1) & (se_vals > 0) & (se_vals < 1)
        z_sp = stats.norm.ppf(sp_vals[mask])
        z_se = stats.norm.ppf(se_vals[mask])
        
        slope, intercept, r_val, p_val, std_err = stats.linregress(z_se, z_sp)
        
        z_se_grid = np.linspace(-5, 5, 512)
        z_sp_grid = intercept + slope * z_se_grid
        
        self.sensitivities = stats.norm.cdf(z_se_grid)
        self.specificities = stats.norm.cdf(z_sp_grid)
        
        sort_idx = np.argsort(1 - self.specificities)
        self.auc_val = auc(1 - self.specificities[sort_idx], self.sensitivities[sort_idx])

    def __str__(self):
        return (f"Call:\nsmooth.roc(rocobj)\n\n"
                f"Data: aSAH$s100b in {len(self.roc.controls)} controls (aSAH$outcome = Good) < "
                f"{len(self.roc.cases)} cases (aSAH$outcome = Poor).\n"
                f"Smoothing: binormal \n"
                f"Area under the curve: {self.auc_val:.4f}")

# r2py:entity:roc
def roc(response, predictor):
    return RocObject(response, predictor)

# r2py:entity:print_1
def smooth(roc_obj):
    return SmoothedRocObject(roc_obj)

# r2py:entity:print_3
def ci(roc_obj):
    cases = roc_obj.cases
    controls = roc_obj.controls
    n_case = len(cases)
    n_ctrl = len(controls)
    
    v_case = []
    for i in range(n_case):
        case_val = cases[i]
        less = np.sum(controls < case_val)
        tied = np.sum(controls == case_val)
        v_case.append((less + 0.5 * tied) / n_ctrl)
        
    v_ctrl = []
    for j in range(n_ctrl):
        ctrl_val = controls[j]
        less = np.sum(cases < ctrl_val)
        tied = np.sum(cases == ctrl_val)
        v_ctrl.append((less + 0.5 * tied) / n_case)
        
    v_case = np.array(v_case)
    v_ctrl = np.array(v_ctrl)
    
    auc_val = roc_obj.auc_val
    var_case = np.var(v_case, ddof=1) / n_case
    var_ctrl = np.var(v_ctrl, ddof=1) / n_ctrl
    se = np.sqrt(var_case + var_ctrl)
    
    low = auc_val - 1.96 * se
    high = auc_val + 1.96 * se
    
    return f"AUC: {auc_val:.4f} 95% CI: {low:.4f} - {high:.4f}"

# Print a roc object:
# r2py:entity:rocobj
rocobj = roc(aSAH['outcome'], aSAH['s100b'])
# r2py:entity:print
print(rocobj)

# Print a smoothed roc object
# r2py:entity:print_1
print(smooth(rocobj))

# implicit printing
# r2py:entity:roc
print(roc(aSAH['outcome'], aSAH['s100b']))

# Print an auc and a ci object, from the ROC object or calling
# the dedicated function:
# r2py:entity:print_2
print(rocobj.auc)
# r2py:entity:print_3
print(ci(rocobj))