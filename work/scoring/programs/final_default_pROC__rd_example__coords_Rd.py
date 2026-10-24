import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import interp1d

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:suppressPackageStartupMessages
# (No-op in Python)

# r2py:entity:import_pROC
# (Handled by implementing roc and coords)

def calculate_metrics(response, predictor, threshold, percent=False):
    resp = pd.Series(response)
    pred = pd.Series(predictor)
    levels = sorted(resp.unique())
    control_val, case_val = levels[0], levels[1]
    
    tp = ((pred >= threshold) & (resp == case_val)).sum()
    fp = ((pred >= threshold) & (resp == control_val)).sum()
    fn = ((pred < threshold) & (resp == case_val)).sum()
    tn = ((pred < threshold) & (resp == control_val)).sum()
    
    se = (tp / (tp + fn)) * (100 if percent else 1)
    sp = (tn / (tn + fp)) * (100 if percent else 1)
    acc = ((tp + tn) / (tp + tn + fp + fn)) * (100 if percent else 1)
    ppv = (tp / (tp + fp)) * (100 if percent else 1) if (tp + fp) > 0 else np.nan
    npv = (tn / (tn + fn)) * (100 if percent else 1) if (tn + fn) > 0 else np.nan
    
    metrics = {
        'threshold': threshold,
        'specificity': sp,
        'sensitivity': se,
        'accuracy': acc,
        'tn': tn, 'tp': tp, 'fn': fn, 'fp': fp,
        'npv': npv, 'ppv': ppv,
        'fdr': (fp / (tp + fp)) * 100 if (tp + fp) > 0 else np.nan,
        'fpr': (fp / (fp + tn)) * (100 if percent else 1),
        'tpr': se,
        'tnr': sp,
        'fnr': (fn / (fn + tp)) * (100 if percent else 1),
        '1-specificity': (fp / (fp + tn)) * (100 if percent else 1),
        '1-sensitivity': (fn / (fn + tp)) * (100 if percent else 1),
        '1-accuracy': (100 if percent else 1) - acc,
        '1-npv': (100 if percent else 1) - npv,
        '1-ppv': (100 if percent else 1) - ppv,
        'precision': ppv,
        'recall': se,
        'lr_pos': (se / (100 - sp)) if percent else (se / (1 - sp)),
        'lr_neg': ((100 - se) / sp) if percent else ((1 - se) / sp)
    }
    return metrics

def roc(response, predictor, percent=False):
    resp = pd.Series(response)
    pred = pd.Series(predictor)
    levels = sorted(resp.unique())
    control_val, case_val = levels[0], levels[1]
    
    # Use all unique values for thresholds to match R
    thresholds = np.unique(pred)
    thresholds = np.sort(thresholds)[::-1]
    
    sensitivities = []
    specificities = []
    
    cases = pred[resp == case_val]
    controls = pred[resp == control_val]
    
    for t in thresholds:
        se = (cases >= t).sum() / len(cases) * (100 if percent else 1)
        sp = (controls < t).sum() / len(controls) * (100 if percent else 1)
        sensitivities.append(se)
        specificities.append(sp)
        
    # pROC boundaries
    sensitivities = [100.0 if percent else 1.0] + sensitivities + [0.0]
    specificities = [0.0] + specificities + [100.0 if percent else 1.0]
    thresholds = [np.inf] + list(thresholds) + [-np.inf]

    return {
        'sensitivities': np.array(sensitivities),
        'specificities': np.array(specificities),
        'thresholds': np.array(thresholds),
        'percent': percent,
        'response': response,
        'predictor': predictor,
        'controls': controls.values,
        'cases': cases.values
    }

def coords(roc_obj, x=None, input="threshold", ret=("threshold", "specificity", "sensitivity"), 
            best_method="youden", best_weights=(1, 0.5)):
    
    se = roc_obj['sensitivities']
    sp = roc_obj['specificities']
    thres = roc_obj['thresholds']
    
    if x is None or x == "all":
        res = pd.DataFrame({'threshold': thres, 'sensitivity': se, 'specificity': sp})
        if ret == "all": return res
        if isinstance(ret, (list, tuple)):
            return res[[c for c in res.columns if c in ret]]
        elif isinstance(ret, str):
            return res[[ret]] if ret in res.columns else res
        return res

    if x == "best":
        if best_method == "youden":
            offset = 100 if roc_obj['percent'] else 1
            score = best_weights[0] * se + best_weights[1] * sp
            if best_weights == (1, 0.5): score = se + sp - offset
            idx = np.argmax(score)
        elif best_method == "closest.topleft":
            top_left = 100 if roc_obj['percent'] else 1
            dist = np.sqrt((top_left - se)**2 + (top_left - sp)**2)
            idx = np.argmin(dist)
        else:
            idx = 0
        
        best_t = thres[idx]
        metrics = calculate_metrics(roc_obj['response'], roc_obj['predictor'], best_t, roc_obj['percent'])
        
        # Youden/Closest distance for ret="all"
        metrics['youden'] = se[idx] + sp[idx] - (100 if roc_obj['percent'] else 1)
        metrics['closest.topleft'] = np.sqrt(( (100 if roc_obj['percent'] else 1) - se[idx])**2 + ( (100 if roc_obj['percent'] else 1) - sp[idx])**2)
        
        res = pd.DataFrame([metrics])
        
        if ret == "all":
            return res
        if isinstance(ret, (list, tuple)):
            return res[[r for r in ret if r in res.columns]]
        elif isinstance(ret, str):
            return res[[ret]] if ret in res.columns else res
        return res

    if input == "threshold":
        idx = np.argmin(np.abs(thres - x))
    elif input in ["sensitivity", "se"]:
        idx = np.argmin(np.abs(se - x))
    elif input in ["specificity", "sp"]:
        idx = np.argmin(np.abs(sp - x))
    else:
        idx = 0
        
    res = pd.DataFrame({'threshold': [thres[idx]], 'sensitivity': [se[idx]], 'specificity': [sp[idx]]})
    if isinstance(ret, (list, tuple)):
        return res[[c for c in res.columns if c in ret]]
    elif isinstance(ret, str):
        return res[[ret]] if ret in res.columns else res
    return res

def smooth(roc_obj, n=512):
    scale = 1/100 if roc_obj['percent'] else 1
    se_norm = norm.ppf(np.clip(roc_obj['sensitivities'] * scale, 1e-7, 1-1e-7))
    sp_norm = norm.ppf(np.clip(roc_obj['specificities'] * scale, 1e-7, 1-1e-7))
    mask = np.isfinite(se_norm) & np.isfinite(sp_norm)
    poly = np.polyfit(se_norm[mask], sp_norm[mask], 1)
    se_grid = np.linspace(0, 1, n)
    se_norm_grid = norm.ppf(np.clip(se_grid, 1e-7, 1-1e-7))
    sp_norm_grid = poly[0] * se_norm_grid + poly[1]
    sp_grid = norm.cdf(sp_norm_grid)
    return {
        'sensitivities': se_grid * (100 if roc_obj['percent'] else 1),
        'specificities': sp_grid * (100 if roc_obj['percent'] else 1),
        'thresholds': np.linspace(np.nanmax(roc_obj['thresholds']), np.nanmin(roc_obj['thresholds']), n),
        'percent': roc_obj['percent']
    }

# r2py:entity:data
# aSAH is loaded by shim

# r2py:entity:roc.s100b
roc_s100b = roc(aSAH['outcome'], aSAH['s100b'], percent=True)

# r2py:entity:coords
print(coords(roc_s100b, 0.55))

# r2py:entity:coords_1
print(coords(roc_s100b, 50, input="sensitivity"))

# r2py:entity:coords_2
print(coords(roc_s100b, 50, "se"))

# r2py:entity:coords_3
smoothed_s100b = smooth(roc_s100b)
print(coords(smoothed_s100b, 90, "specificity"))

# r2py:entity:cc
cc = coords(roc_s100b, "all", ret="sensitivity")
# r2py:entity:print
print(cc['sensitivity'])

# r2py:entity:coords_4
print(coords(roc_s100b, "best", ret="threshold"))

# r2py:entity:roc.ndka
roc_ndka = roc(aSAH['outcome'], aSAH['ndka'], percent=True)

# r2py:entity:coords_5
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))

# r2py:entity:coords_6
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# r2py:entity:coords_7
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=(50, 0.2)))

# r2py:entity:coords_8
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=(5, 0.2)))

# r2py:entity:plot
plt.figure()
plt.plot(100 - roc_ndka['specificities'], roc_ndka['sensitivities'])
plt.xlabel("1 - Specificity")
plt.ylabel("Sensitivity")
plt.title("ROC Curve ndka")
plt.show()

# r2py:entity:coords_9
print(coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"]))

# r2py:entity:coords_10
print(coords(roc_s100b, "best", ret="all"))

# r2py:entity:plot_1
all_coords_ndka = coords(roc_ndka, "all")
plt.figure()
plt.plot(all_coords_ndka['threshold'], all_coords_ndka['specificity'] + all_coords_ndka['sensitivity'])
plt.xscale('log')
plt.title("Spec + Sens vs Threshold")
plt.show()

# r2py:entity:plot_2
cases_ndka = aSAH[aSAH['outcome'] == "Poor"]['ndka']
controls_ndka = aSAH[aSAH['outcome'] == "Good"]['ndka']
threshs = np.unique(aSAH['ndka'])
precisions, recalls = [], []
for t in threshs:
    tp = (cases_ndka >= t).sum()
    fp = (controls_ndka >= t).sum()
    fn = (cases_ndka < t).sum()
    precisions.append(tp / (tp + fp) if (tp + fp) > 0 else 1)
    recalls.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
plt.figure()
plt.plot(np.array(recalls)*100, np.array(precisions)*100)
plt.ylim(0, 100)
plt.title("Precision-Recall Curve")
plt.show()

# r2py:entity:plot_3
plt.figure()
plt.plot(100 - roc_ndka['specificities'], roc_ndka['sensitivities'])
plt.title("TPR vs FPR")
plt.show()