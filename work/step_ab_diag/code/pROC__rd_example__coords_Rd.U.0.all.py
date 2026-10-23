import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve, accuracy_score, precision_score, recall_score
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

def get_roc_df(y_true, y_score):
    # sklearn roc_curve returns thresholds sorted descending
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    # pROC thresholds are the actual values. 
    # roc_curve adds a threshold > max(y_score) to ensure FPR=0, TPR=0.
    # We create a DataFrame that mirrors pROC's structure (percent=True)
    df = pd.DataFrame({
        'threshold': thresholds,
        'sensitivity': tpr * 100,
        'specificity': (1 - fpr) * 100
    })
    return df

def coords(roc_df, x=None, input="threshold", ret="all", best_method="youden", best_weights=None):
    # Simplified implementation of pROC::coords
    df = roc_df.copy()
    
    if x == "best":
        if best_method == "youden":
            w1 = best_weights[0] if best_weights else 1.0
            w2 = best_weights[1] if best_weights else 1.0
            # Youden: J = w1*Sens + w2*Spec - (w1+w2)*100 (standardized to match R)
            # In R, youden is Sens + Spec - 100. With weights: w1*Sens + w2*Spec - constant
            score = w1 * df['sensitivity'] + w2 * df['specificity']
            idx = score.idxmax()
        elif best_method == "closest.topleft":
            # Distance to (0, 100) in ROC space
            # FPR is (100-Spec)/100, TPR is Sens/100
            # dist = sqrt( (FPR)^2 + (1-TPR)^2 )
            w1 = best_weights[0] if best_weights else 1.0
            w2 = best_weights[1] if best_weights else 1.0
            fpr = (100 - df['specificity']) / 100
            tpr = df['sensitivity'] / 100
            dist = np.sqrt(w1 * (fpr**2) + w2 * ((1 - tpr)**2))
            idx = dist.idxmin()
        else:
            idx = 0
        
        best_row = df.loc[idx]
        
        if ret == "all":
            # Return a series with all calculated metrics
            # Recalculate accuracy, precision, recall for this specific threshold
            t = best_row['threshold']
            # We need the original data to calculate these
            # Since we don't have it in the function, we'll have to handle it carefully 
            # in the main script or pass it. For this specific exercise, we can rely on
            # the main script's access to aSAH.
            return best_row
        elif isinstance(ret, list):
            return {k: best_row[k] if k in best_row else None for k in ret}
        elif isinstance(ret, str):
            return best_row[ret]
        return best_row

    if input == "threshold":
        # Find threshold closest to x
        idx = (np.abs(df['threshold'] - x)).idxmin()
        return df.loc[[idx]]
    elif input in ["sensitivity", "se"]:
        # Interpolate to find threshold for specific sensitivity
        f = interp1d(df['sensitivity'], df['threshold'], fill_value="extrapolate")
        thresh = f(x)
        # Return a DataFrame to match R output
        return pd.DataFrame({'threshold': [thresh], 'specificity': [df.loc[(np.abs(df['sensitivity'] - x)).idxmin(), 'specificity']], 'sensitivity': [x]})
    elif input in ["specificity", "sp"]:
        f = interp1d(df['specificity'], df['threshold'], fill_value="extrapolate")
        thresh = f(x)
        return pd.DataFrame({'threshold': [thresh], 'specificity': [x], 'sensitivity': [df.loc[(np.abs(df['specificity'] - x)).idxmin(), 'sensitivity']]})
    
    if x == "all":
        if ret == "sensitivity":
            return pd.DataFrame({'sensitivity': df['sensitivity']})
        return df

# Create ROC curves
roc_s100b = get_roc_df(aSAH['outcome'], aSAH['s100b'])
roc_ndka = get_roc_df(aSAH['outcome'], aSAH['ndka'])

# Get the coordinates of S100B threshold 0.55
print(coords(roc_s100b, 0.55))

# Get the coordinates at 50% sensitivity
print(coords(roc_s100b, x=50, input="sensitivity"))
print(coords(roc_s100b, 50, "se"))

# Works with smoothed ROC curves (Approximated by using the ROC DataFrame)
print(coords(roc_s100b, 90, "specificity"))

# Get the sensitivities for all thresholds
cc = coords(roc_s100b, "all", ret="sensitivity")
print(cc['sensitivity'].values)

# Get the best threshold
print(coords(roc_s100b, "best", ret="threshold"))

# Get the best threshold according to different methods
print(coords(roc_ndka, "best", ret="threshold", best_method="youden"))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# and with different weights
print(coords(roc_ndka, "best", ret="threshold", best_method="youden", best_weights=[50, 0.2]))
print(coords(roc_ndka, "best", ret="threshold", best_method="closest.topleft", best_weights=[5, 0.2]))

# Plotting (simulated via prints as per environment constraints, but structured for plotnine/matplotlib)
# plot(roc.ndka, print.thres="best", ...)
print("Plotting ROC curve for ndka...")

# Return more values
res_best = coords(roc_s100b, "best", ret=["threshold", "specificity", "sensitivity", "accuracy", "precision", "recall"])
# For the specific ones like accuracy, precision, recall, we need to use the threshold on the original data
t_best = coords(roc_s100b, "best", ret="threshold")
preds = (aSAH['s100b'] >= t_best).astype(int)
res_best['accuracy'] = accuracy_score(aSAH['outcome'], preds) * 100
res_best['precision'] = precision_score(aSAH['outcome'], preds) * 100
res_best['recall'] = recall_score(aSAH['outcome'], preds) * 100
print(res_best)

# Return all values
print(coords(roc_s100b, "best", ret="all"))

# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
all_coords_ndka = coords(roc_ndka, "all")
plot_data_1 = all_coords_ndka.copy()
plot_data_1['sum_spec_sens'] = plot_data_1['specificity'] + plot_data_1['sensitivity']
plot_data_1 = plot_data_1[np.isfinite(plot_data_1['threshold'])]
plt.figure()
plt.semilogx(plot_data_1['threshold'], plot_data_1['sum_spec_sens'])
plt.xlabel('threshold')
plt.ylabel('specificity + sensitivity')
plt.show()

# Plot the Precision-Recall curve
prec, rec, _ = precision_recall_curve(aSAH['outcome'], aSAH['ndka'])
plt.figure()
plt.plot(rec * 100, prec * 100)
plt.ylim(0, 100)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
plt.figure()
plt.plot(100 - roc_ndka['specificity'], roc_ndka['sensitivity'])
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()