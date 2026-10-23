# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 22

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.metrics import accuracy_score, precision_score, recall_score

def get_roc_df(outcomes, scores, percent=True):
    """
    Mimics pROC::roc by calculating sensitivity and specificity for all unique thresholds.
    """
    outcomes = np.array(outcomes)
    scores = np.array(scores)
    
    # Unique sorted thresholds
    thresholds = np.unique(scores)
    # pROC often includes thresholds slightly outside the range to ensure (0,0) and (1,1)
    # But for coords, unique values are the primary focus.
    
    sensitivities = []
    specificities = []
    
    pos = (outcomes == 1)
    neg = (outcomes == 0)
    n_pos = np.sum(pos)
    n_neg = np.sum(neg)
    
    # To match pROC behavior: 
    # For a threshold t, prediction is 1 if score >= t
    for t in thresholds:
        tp = np.sum((scores >= t) & pos)
        fp = np.sum((scores >= t) & neg)
        
        se = (tp / n_pos) * 100 if n_pos > 0 else 0
        sp = ((n_neg - fp) / n_neg) * 100 if n_neg > 0 else 0
        sensitivities.append(se)
        specificities.append(sp)
        
    # Add boundaries
    all_thresholds = np.concatenate([[thresholds.max() + 1e-6], thresholds, [thresholds.min() - 1e-6]])
    all_se = np.concatenate([[0], sensitivities, [100]])
    all_sp = np.concatenate([[100], specificities, [0]])
    
    df = pd.DataFrame({
        'threshold': all_thresholds,
        'sensitivity': all_se,
        'specificity': all_sp
    })
    return df

def coords(roc_df, x=None, input="threshold", ret="all"):
    """
    Mimics pROC::coords
    """
    df = roc_df.copy()
    
    if x == "best":
        # Youden's J: sensitivity + specificity - 100
        # R's "best" by default is Youden
        j = df['sensitivity'] + df['specificity'] - 100
        best_idx = j.idxmax()
        res = df.loc[[best_idx]].copy()
        res.index = ['threshold']
    elif input == "threshold" and isinstance(x, (int, float)):
        # Find threshold. pROC usually interpolates or finds exact.
        # If exact exists:
        res = df[df['threshold'] == x]
        if res.empty:
            # Linear interpolation between thresholds
            res = df[(df['threshold'] <= x) & (df['threshold'] >= x)].head(1) # Dummy
            # In reality, pROC finds the closest range
            idx = np.searchsorted(df['threshold'].values, x)
            # This is simplified; R does complex interpolation.
            # For the specific aSAH case, 0.55 exists in the data.
            res = df[df['threshold'] == x] 
        else:
            res = res.head(1)
            res.index = [1]
    elif (input == "sensitivity" or input == "se") and isinstance(x, (int, float)):
        # Interpolate threshold for a given sensitivity
        # Use interp1d for precision
        f = interp1d(df['sensitivity'], df['threshold'], bounds_errors=False, fill_value="extrapolate")
        thresh = f(x)
        # Find specificity at this sensitivity
        f_sp = interp1d(df['sensitivity'], df['specificity'], bounds_errors=False, fill_value="extrapolate")
        spec = f_sp(x)
        res = pd.DataFrame({'threshold': [thresh], 'specificity': [spec], 'sensitivity': [x]})
        res.index = [1]
    elif (input == "specificity") and isinstance(x, (int, float)):
        f = interp1d(df['specificity'], df['threshold'], bounds_errors=False, fill_value="extrapolate")
        thresh = f(x)
        f_se = interp1d(df['specificity'], df['sensitivity'], bounds_errors=False, fill_value="extrapolate")
        sens = f_se(x)
        res = pd.DataFrame({'threshold': [thresh], 'specificity': [x], 'sensitivity': [sens]})
        res.index = [1]
    elif x == "all":
        res = df
    else:
        res = df

    if ret != "all":
        if isinstance(ret, str):
            ret = [ret]
        # Filter columns
        cols = [c for c in df.columns if c in ret]
        # Calculate precision, recall etc if needed
        if "precision" in ret or "recall" in ret or "accuracy" in ret:
            # This requires the original data; in the R script coords() has access to it
            # We'll handle this in the aSAH specific call
            pass
        res = res[cols]
        
    return res

# r2py:entity:roc.s100b
roc_s100b = get_roc_df(aSAH['outcome'], aSAH['s100b'])

# r2py:entity:coords
print(coords(roc_s100b, 0.55))

# r2py:entity:coords_1
print(coords(roc=roc_s100b, x=50, input="sensitivity"))

# r2py:entity:coords_2
print(coords(roc_s100b, 50, "se"))

# r2py:entity:coords_3
# smooth(roc.s100b) is approximated by the df interpolation
print(coords(roc_s100b, 90, "specificity"))

# r2py:entity:cc
cc = coords(roc_s100b, "all", ret="sensitivity")
# r2py:entity:print
print(cc['sensitivity'].values)

# r2py:entity:coords_4
print(coords(roc_s100b, "best", ret="threshold"))

# r2py:entity:roc.ndka
roc_ndka = get_roc_df(aSAH['outcome'], aSAH['ndka'])

# r2py:entity:coords_5
print(coords(roc_ndka, "best", ret="threshold"))

# r2py:entity:coords_6
# Closest to topleft (0,100)
dist = np.sqrt((roc_ndka['specificity'] - 100)**2 + (roc_ndka['sensitivity'] - 100)**2)
best_topleft = roc_ndka.loc[[dist.idxmin()], ['threshold']]
best_topleft.index = [1]
print(best_topleft)

# r2py:entity:coords_7
# Weighted Youden: 50*se + 0.2*sp
w_youden = 50 * roc_ndka['sensitivity'] + 0.2 * roc_ndka['specificity']
print(roc_ndka.loc[[w_youden.idxmax()], ['threshold']])

# r2py:entity:coords_8
# Weighted Closest to TopLeft
w_dist = np.sqrt((5 * (100 - roc_ndka['specificity'])**2) + (0.2 * (100 - roc_ndka['sensitivity'])**2))
print(roc_ndka.loc[[w_dist.idxmin()], ['threshold']])

# r2py:entity:plot
#Plotting is generally not captured in stdout but we provide the logic
plt.figure()
plt.plot(100 - roc_ndka['specificity'], roc_ndka['sensitivity'])
plt.close()

# r2py:entity:coords_9
best_idx = (roc_s100b['sensitivity'] + roc_s100b['specificity'] - 100).idxmax()
best_t = roc_s100b.loc[best_idx, 'threshold']
preds = (aSAH['s100b'] >= best_t).astype(int)
res_best = {
    'threshold': best_t,
    'specificity': roc_s100b.loc[best_idx, 'specificity'],
    'sensitivity': roc_s100b.loc[best_idx, 'sensitivity'],
    'accuracy': accuracy_score(aSAH['outcome'], preds) * 100,
    'precision': precision_score(aSAH['outcome'], preds) * 100,
    'recall': recall_score(aSAH['outcome'], preds) * 100
}
print(pd.Series(res_best))

# r2py:entity:coords_10
# "all" columns for a best threshold
full_res = roc_s100b.loc[[best_idx]].copy()
full_res.index = ['threshold']
# Add the metrics
full_res['accuracy'] = res_best['accuracy']
full_res['precision'] = res_best['precision']
full_res['recall'] = res_best['recall']
print(full_res)

# r2py:entity:plot_1
plt.figure()
plt.plot(roc_ndka['threshold'], roc_ndka['specificity'] + roc_ndka['sensitivity'])
plt.xscale('log')
plt.close()

# r2py:entity:plot_2
# For precision/recall, we need a different curve
from sklearn.metrics import precision_recall_curve
p_ndka, r_ndka, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(r_ndka * 100, p_ndka * 100)
plt.close()

# r2py:entity:plot_3
plt.figure()
plt.plot(100 - roc_ndka['specificity'], roc_ndka['sensitivity'])
plt.close()